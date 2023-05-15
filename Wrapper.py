import Mapa as mp
from interfaces import InitializationInterface
import Qlearning as Q
import FPA as f
import APF as a
import WOA as w


class weirdWrapper(InitializationInterface):
    def __init__(self, flag=False) -> None:
        self.apf = a.APF()
        self.fpa = f.FPA()
        self.woa = w.WOA()
        self.flag = flag

    def initialize(self, map, gazebo):
        Qapf = self.apf.initialize(map, gazebo)
        if self.flag:
            self.Q = self.fpa.initialize(map, gazebo, Qapf)
        else:
            self.Q = self.woa.initialize(map, gazebo, Qapf)
        return self.Q.copy()

    def save(self, path="data.txt", full=True, Q=True):
        self.apf.save(path, full, Q)
        if self.flag:
            self.fpa.save(path, full, Q)
        else:
            self.woa.save(path, full, Q)
