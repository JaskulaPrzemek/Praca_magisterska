from abc import ABC, abstractmethod

class InitializationInterface(ABC):

    @abstractmethod
    def initialize(self, map,gazebo):
        pass
    @abstractmethod
    def save(self,path="data.txt",full=True,Q=True):
        pass