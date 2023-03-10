import numpy as np
import random
import math
from interfaces import InitializationInterface
import Qlearning as Q
import tensorflow as tf
class NN(InitializationInterface):
    def __init__(self):
        self.model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(404,)),
        tf.keras.layers.Dense(404, activation='relu'),
        tf.keras.layers.Dense(404, activation='relu'),
        tf.keras.layers.Dense(400)
        ])
    def initialize(self,map,gazebo):
        pass
    def save(self,path=""):
        pass