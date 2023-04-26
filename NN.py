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

    def createTrainData(self):
        maps = []
        Qmatrices = []
        for _ in range(self.InputTrainNumber):
            self.Qlearning.createMap(4)
            tempMap = self.Qlearning.map.cMap.copy()
            tempMap = tempMap * 255
            x, y = self.Qlearning.map.startingPoint
            tempMap[x][y] = 40
            x, y = self.Qlearning.map.target
            tempMap[x][y] = 200
            maps.append(tempMap)
            self.Qlearning.learn()
            Qmatrices.append(self.Qlearning.Q.copy())
        self.TrainX = np.array(maps)
        self.TrainY = np.array(Qmatrices)
        np.save("TrainingData/Training_Q", self.TrainY)
        np.save("TrainingData/Training_Maps", self.TrainX)
        print("Finished generating")

    def loadTrainingData(self):
        self.TrainY = np.load("TrainingData/Training_Q.npy")
        self.TrainX = np.load("TrainingData/Training_Maps.npy")
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
