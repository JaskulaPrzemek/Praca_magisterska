import numpy as np
import random
import math
from interfaces import InitializationInterface
import Qlearning as Q
import Mapa as mp
import tensorflow as tf


class NN(InitializationInterface):

    def __init__(self):
        self.model = tf.keras.Sequential([
            #map is 21*21,start is 2, finish is 2
            tf.keras.layers.InputLayer(input_shape=(445,)),
            tf.keras.layers.Dense(445, activation='relu'),
            tf.keras.layers.Dense(445, activation='relu'),
            # output is the Q which is 20*20*4
            tf.keras.layers.Dense(1600, activation='relu')
        ])
        self.InputTrainNumber = 64*1
        self.average_nr = 1
        self.batch_size=2
        self.Qlearning = Q.Qlearning()
        self.Qlearning.setEpsilon(0.05)
        self.Qlearning.setDisableInit()

    def custom_loss(self, y_true, y_pred):
        avg = tf.py_function(func=self.run_average_steps, inp=[y_true, y_pred], Tout=[tf.float64])
        print(avg)
        return avg

    def run_average_steps(self, map_rep, Q_list):
        avg = []
        print("calculating loss")
        for map_list, Q_matrix in zip(map_rep.numpy(),Q_list.numpy()):
            suma = 0
            Q_matrix = np.reshape(Q_matrix, (400, 4))
            map_list = np.reshape(map_list, (445))
            self.Qlearning.map.loadListRep(map_list)
            for i in range(self.average_nr):
                print(f"Run {i}")
                self.Qlearning.Q = np.copy(Q_matrix)
                self.Qlearning.learn()
                steps = self.Qlearning.steps
                # print(steps)
                suma += sum(steps)/len(steps)
            avg.append(suma/self.average_nr)
            # print(avg)
        #avg = tf.constant(avg,dtype=tf.float64)
        print (avg)
        return avg

    def createTrainData(self):
        xdata = []
        ydata = [22*100]*self.InputTrainNumber
        mapa = mp.Map()
        with open("Training_maps.txt", 'a') as file:
            for i in range(self.InputTrainNumber):
                mapa.createRandomMap()
                v = mapa.getListRep()
                file.write(f"{str(v)} \n")
                xdata.append(v)

        self.TrainX = xdata
        self.TrainY = ydata
        print("Finished generating")

    def loadTrainingData(self):
        xdata = []
        nr = 0
        with open("Training_maps.txt", 'r') as file:
            for line in file:
                xdata.append(eval(line))
                nr += 1
                if nr >= self.InputTrainNumber:
                    break
            # print(xdata)
        # ydata=[22*100]*len(xdata)
        self.TrainX = xdata
        # self.TrainY=ydata
        print("Finished loading")

    def train(self):
        self.model.compile(optimizer='adam', run_eagerly=False,
                           loss=self.custom_loss)
        print("Finished compiling")
        steps = int( np.ceil(len(self.TrainX) / self.batch_size) )
        self.model.fit(self.TrainX, self.TrainX,
                       epochs=5, batch_size=self.batch_size, verbose=2,steps_per_epoch=steps)

    def save_model(self, path="model"):
        self.model.save(path)

    def load(self, path="model"):
        self.model = tf.keras.models.load_model(path)

    def initialize(self, map, gazebo):
        pass

    def save(self, path="data.txt", full=True, Q=True):
        pass


network = NN()
network.InputTrainNumber = 8*1
network.loadTrainingData()
network.train()
#network.save_model()
