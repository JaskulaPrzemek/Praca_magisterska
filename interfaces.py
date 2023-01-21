from abc import ABC, abstractmethod

class InitializationInterface(ABC):

    @abstractmethod
    def initialize(self, map,gazebo):
        pass