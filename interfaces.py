from abc import ABC, abstractmethod


class InitializationInterface(ABC):
    @abstractmethod
    def initialize(self, map, gazebo):
        pass

    @abstractmethod
    def save(self, path="data.txt", full=True, Q=True):
        pass

    def name(self):
        d = {v: k for k, v in globals().items()}
        return d[self]
