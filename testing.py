import math

try:
    import rospy
    import gazeboCommunication as gzlib
except ImportError:
    pass
import matplotlib.pyplot as plt

import Mapa as mp
import Qlearning as Q
import FPA as f
import APF as a
import WOA as w
import NN as n
import random
import time
import numpy as np


def avg(lst):
    return sum(lst) / len(lst)


nn = n.NN()
nn.load("Models/16000/sqdModelMSEBig.keras")
Qleran = Q.Qlearning()
Qleran.createMap(2)
Qleran.setEpsilon(0.05)
Qleran.setStrategy(nn)
Qleran.learn()
print(Qleran.time)
# l.setStrategy(fpa)
# l.learn()
# print(l.time)
# l.setEpsilon(0.01)
# l.setStrategy(woa)
# l.learn()
# print(l.time)
# print(l.Qtime)
# path=l.plotPath(show)
# steps=l.plotSteps(show)
# l.setStrategy(apf)
# l.learn()
# print(l.time)
# plt.show()
# apf.showAttract()
# l.plotPath(show,path)
# l.plotSteps(show,steps)
# plt.show()
