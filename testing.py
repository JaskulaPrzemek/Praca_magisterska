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


woa = w.WOA()
apf = a.APF()
fpa = f.FPA()
Qleran = Q.Qlearning()
nn = n.NN()
nn.InputTrainNumber = 16
# nn.createTrainData()
# nn.loadTrainingData()
# print(type(nn.TrainX))
# print(type(nn.TrainY))
for _ in range(7):
    Qleran.createMap(4)
    # Qleran.map.viewMap()
    Qleran.setEpsilon(0.05)
    Qleran.setStrategy(apf)
    Qleran.learn()
    print(Qleran.time)
    print(Qleran.Qtime)
    Qleran.plotPath()
    # Qleran.setStrategy(fpa)
    # Qleran.learn()
    # print(Qleran.time)
    # print(Qleran.Qtime)
    # Qleran.plotPath()
    # Qleran.setStrategy(woa)
    # Qleran.learn()
    # print(Qleran.time)
    # print(Qleran.Qtime)
    # Qleran.plotPath()
# print(Qleran.steps)
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
