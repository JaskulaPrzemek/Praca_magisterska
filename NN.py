import json
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
        self.generator()
        self.eagerly = False
        self.InputTrainNumber = 64 * 1
        self.average_nr = 1
        self.batch_size = 2
        self.Qlearning = Qmodule.Qlearning()
        self.epochs = 55
        self.eps = 0.05
        self.Qlearning.setEpsilon(0.05)
        self.optimizer = "adam"
        self.loss = tf.keras.losses.MeanAbsoluteError()
        # self.Qlearning.setDisableInit()

    def generator(self):
        inputs = tf.keras.layers.Input(shape=(64, 64, 1))
        OUTPUT_CHANNELS = 4
        rescaler = tf.keras.layers.Rescaling(scale=1.0 / 255)
        # Based on Pix2Pix generator
        down_stack = [
            self.downsample(32, 4, apply_batchnorm=False),
            self.downsample(64, 4),
            self.downsample(128, 4),
            self.downsample(256, 4),
            self.downsample(256, 4),
            self.downsample(256, 4),
        ]
        up_stack = [
            self.upsample(256, 4, apply_dropout=True),
            self.upsample(256, 4, apply_dropout=True),
            self.upsample(256, 4, apply_dropout=True),
            self.upsample(128, 4, apply_dropout=True),
            self.upsample(64, 4, apply_dropout=True),
        ]
        initializer = tf.random_normal_initializer(0.0, 0.02)
        last = tf.keras.layers.Conv2DTranspose(
            OUTPUT_CHANNELS,
            4,
            strides=2,
            padding="same",
            kernel_initializer=initializer,
            activation="tanh",
        )
        x = inputs
        x = rescaler(x)
        skips = []
        for down in down_stack:
            x = down(x)
            skips.append(x)
        skips = reversed(skips[:-1])
        for up, skip in zip(up_stack, skips):
            x = up(x)
            x = tf.keras.layers.Concatenate()([x, skip])
        x = last(x)
        self.model = tf.keras.Model(inputs=inputs, outputs=x)

    def downsample(
        self, filters, size, pool_size=(2, 2), apply_maxpool=False, apply_batchnorm=True
    ):
        initializer = tf.random_normal_initializer(0.0, 0.02)
        result = tf.keras.Sequential()
        result.add(
            tf.keras.layers.Conv2D(
                filters,
                size,
                strides=2,
                padding="same",
                kernel_initializer=initializer,
                use_bias=False,
            )
        )

        if apply_batchnorm:
            result.add(tf.keras.layers.BatchNormalization())

        result.add(tf.keras.layers.LeakyReLU())
        if apply_maxpool:
            result.add(tf.keras.layers.MaxPooling2D(pool_size=pool_size))

        return result

    def upsample(self, filters, size, apply_dropout=False):
        initializer = tf.random_normal_initializer(0.0, 0.02)

        result = tf.keras.Sequential()
        result.add(
            tf.keras.layers.Conv2DTranspose(
                filters,
                size,
                strides=2,
                padding="same",
                kernel_initializer=initializer,
                use_bias=False,
            )
        )

        result.add(tf.keras.layers.BatchNormalization())

        if apply_dropout:
            result.add(tf.keras.layers.Dropout(0.5))

        result.add(tf.keras.layers.ReLU())

        return result

    def createTrainData(self, path="Training"):
        maps = []
        Qmatrices = []
        for _ in range(self.InputTrainNumber):
            self.Qlearning.createMap(4)
            tempMap = self.Qlearning.map.cMap.copy()
            tempMap = tempMap * 255
            x, y = self.Qlearning.map.startingPoint
            tempMap[x][y] = 40
            x, y = self.Qlearning.map.target
            tempMap[x][y] = 150
            maps.append(tempMap)
            self.Qlearning.learn()
            Qmatrices.append(self.Qlearning.Q.copy())
        self.TrainX = np.array(maps)
        self.TrainY = np.array(Qmatrices)
        np.save("TrainingData/" + path + "_Q", self.TrainY)
        np.save("TrainingData/" + path + "_Maps", self.TrainX)
        print("Finished generating")

    def loadTrainingData(self, path="Training"):
        self.TrainY = np.load("TrainingData/" + path + "_Q.npy")
        self.TrainX = np.load("TrainingData/" + path + "_Maps.npy")
        print(self.TrainY.shape)
        print("Finished loading")

    def train(self, path="history.json"):
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
        hist_dict = hist.history
        json.dump(hist_dict, open(path, "w"))

    def save_model(self, path="model.keras"):
        self.model.save("Models/" + path)

    def load(self, path="model.keras"):
        self.ModelName = path[:-6]
        self.model = tf.keras.saving.load_model("Models/" + path)

    def initialize(self, map, gazebo):
        output = self.model.predict(map.cMap.reshape(1, map.size[0], map.size[1], 1))
        print(type(output))
        self.Q = output.reshape(map.size[0], map.size[1], 4)
        return self.Q.copy()

    def save(self, path="data.txt", full=True, Q=True):
        with open(path, "a") as file:
            file.write(f"Qi {np.array_str(self.Q)} \n")


# network.model.summary()
# print(network.model.layers[1].get_weights())
# print(network.model.layers[2].get_weights())
# print(network.model.layers[3].get_weights())
if __name__ == "main":
    network = NN()
    network.InputTrainNumber = 16
    network.loadTrainingData()
    network.model.summary()
    network.train()
    network.save_model()
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
