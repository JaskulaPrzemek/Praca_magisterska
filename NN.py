import numpy as np
import random
import math
from interfaces import InitializationInterface
import Qlearning as Qmodule
import Mapa as mp
import tensorflow as tf
from multiprocessing import Process, Queue


class NN(InitializationInterface):
    def __init__(self):
        inputs = tf.keras.layers.Input(shape=(445,))
        x = tf.keras.layers.Dense(445, activation="elu")(inputs)
        x = tf.keras.layers.Dense(1764, activation="elu")(x)
        outputs = tf.keras.layers.Dense(1764, activation="elu")(x)
        self.model = tf.keras.Model(inputs=inputs, outputs=outputs)
        self.eagerly = True
        self.InputTrainNumber = 64 * 1
        self.average_nr = 1
        self.batch_size = 2
        self.Qlearning = Qmodule.Qlearning()
        self.epochs = 15
        self.eps = 0.05
        self.Qlearning.setEpsilon(0.05)
        self.optimizer = "adam"
        self.loss = tf.keras.losses.MeanAbsoluteError()
        # self.Qlearning.setDisableInit()

    def custom_loss(self, y_true, y_pred):
        # avg = tf.py_function(
        #     func=self.run_average_steps, inp=[y_true, y_pred], Tout=[tf.float64]
        # )
        avg = self.run_average_steps(y_true, y_pred)
        # print(avg)

        return tf.constant(avg)

    def run_average_steps(self, map_rep, Q_list):
        avg = []
        print("calculating loss")
        Qlist = [Queue() for _ in range(self.batch_size)]
        # print(Qlist)
        # avg.append(self.batch_size)
        list_of_lists_of_processes = []
        for map_list, q_matrix, q in zip(map_rep.numpy(), Q_list.numpy(), Qlist):
            q_matrix = np.reshape(q_matrix, (441, 4))
            map_list = np.reshape(map_list, (445))
            p_list = [
                Process(
                    target=self.get_avg_step,
                    args=(
                        map_list,
                        q_matrix,
                        q,
                    ),
                )
                for _ in range(self.average_nr)
            ]
            for process in p_list:
                process.start()
            list_of_lists_of_processes.append(p_list)
        for l, q in zip(list_of_lists_of_processes, Qlist):
            for p in l:
                p.join()
            suma = 0
            for _ in range(self.average_nr):
                suma += q.get()
            avg.append(suma / self.average_nr)
            # print(avg)
        # avg = tf.constant(avg,dtype=tf.float64)
        print(avg)
        return avg

    def get_avg_step(self, map_rep, q_matrix, Que):
        # print("process jo")
        q = Qmodule.Qlearning()
        q.setEpsilon(self.eps)
        q.setDisableInit()
        q.Q = np.copy(q_matrix)
        q.map.loadListRep(map_rep)
        q.learn()
        steps = q.steps
        avg = sum(steps) / len(steps)
        Que.put(avg)

    def createTrainData(self):
        xdata = []
        ydata = []
        mapa = mp.Map()
        with open("TrainingData/Training_maps1.txt", "a") as file:
            for _ in range(self.InputTrainNumber):
                mapa.createRandomMap()
                v = mapa.getListRep()
                file.write(f"{str(v)} \n")
                xdata.append(v)
        for map in xdata:
            self.Qlearning.map.loadListRep(map)
            self.Qlearning.learn()
            ydata.append(np.reshape(self.Qlearning.Q, (1764)))

        self.TrainX = np.array(xdata)
        self.TrainY = np.array(ydata)
        np.savetxt("TrainingData/Training_Q1.txt", self.TrainY)
        print("Finished generating")

    def loadTrainingData(self):
        xdata = []
        nr = 0
        with open("TrainingData/Training_maps.txt", "r") as file:
            for line in file:
                x = eval(line)
                xdata.append(x)
                nr += 1
                if nr >= self.InputTrainNumber:
                    break
        # ydata=[22*100]*len(xdata)
        nr = 0
        ydata = np.loadtxt("TrainingData/Training_Q.txt")
        print(ydata.shape)
        self.TrainX = np.array(xdata)
        self.TrainY = ydata[: self.InputTrainNumber, :]
        print(self.TrainY.shape)
        print("Finished loading")

    def train(self):
        # self.model.compile(
        #    optimizer="adam", run_eagerly=self.eagerly, loss=self.custom_loss
        # )
        self.model.compile(
            optimizer=self.optimizer,
            run_eagerly=self.eagerly,
            loss=self.loss,
            metrics=["accuracy"],
        )
        print("Finished compiling")
        steps = int(np.ceil(len(self.TrainX) / self.batch_size))
        print(steps)
        hist = self.model.fit(
            self.TrainX,
            self.TrainY,
            batch_size=self.batch_size,
            verbose=1,
            epochs=self.epochs,
        )
        print(hist)

    def save_model(self, path="model.keras"):
        self.model.save(path)

    def load(self, path="model.keras"):
        self.model = tf.keras.saving.load_model(path)

    def initialize(self, map, gazebo):
        List = map.getListRep()
        output = self.model.predict(tf.reshape(List, (1, 445)))
        self.Q = np.reshape(output, (441, 4))
        return self.Q.copy()

    def save(self, path="data.txt", full=True, Q=True):
        with open(path, "a") as file:
            file.write(f"Qi {np.array_str(self.Q)} \n")


# network.model.summary()
# print(network.model.layers[1].get_weights())
# print(network.model.layers[2].get_weights())
# print(network.model.layers[3].get_weights())


# network.loadTrainingData()
# network.model.summary()
# network.train()
# network.save_model()
# network.load("AdamModelMSE.keras")
# m = mp.Map()
# m.createRandomMap()
# listaa = m.getListRep()
# print(listaa)
# v = network.model.predict(tf.constant(np.reshape(listaa, (1, 445))))
# print(v)
# network.model.summary()
# print(network.model.layers[1].get_weights())
# print(network.model.layers[2].get_weights())
# print(network.model.layers[3].get_weights())
# network.loadTrainingData()
# network.model.summary()
# network.train()
# network.save_model()
