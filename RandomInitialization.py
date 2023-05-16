import Mapa as mp
from interfaces import InitializationInterface
import numpy as np


class randomInit(InitializationInterface):
    def __init__(self) -> None:
        self.gauss = True
        self.Min = -1
        self.Max = 1
        self.loc = 0
        self.scale = 0.1
        self.finalValue = 3

    def initialize(self, map, gazebo):
        size = map.size
        target = map.target
        if self.gauss:
            self.Q = np.random.normal(
                loc=self.loc, scale=self.scale, size=(size[0], size[1], 4)
            )
        else:
            self.Q = np.random.rand(size[0], size[1], 4)
            self.Q = (self.Q * (self.Max - self.Min)) + self.Min
        self.Q[target[0]][target[1]] = self.finalValue
        return self.Q.copy()

    def save(self, path="data.txt", full=True, Q=True):
        with open(path, "a") as file:
            file.write(f"{__name__}: \n")
            if Q:
                file.write(f"Q {np.array_str(self.Q)} \n")
