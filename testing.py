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


class weirdWrapper:
    def __init__(self) -> None:
        self.apf = a.APF()
        self.fpa = f.FPA()
        self.woa = w.WOA()
        self.flag = False

    def initialize(self, map, gazebo):
        Qapf = self.apf.initialize(map, gazebo)
        if self.flag:
            self.Q = self.fpa.initialize(map, gazebo, Qapf)
        else:
            self.Q = self.woa.initialize(map, gazebo, Qapf)
        return self.Q.copy()


woa = w.WOA()
apf = a.APF()
fpa = f.FPA()
Qleran = Q.Qlearning()
nn = n.NN()
testWrap = weirdWrapper()
testWrap1 = weirdWrapper()
testWrap1.flag = True
strats = [None, apf, fpa, woa, testWrap, testWrap1]
strats1 = [testWrap, testWrap1]
strats2 = [None, fpa]
nn.InputTrainNumber = 16
testWrap.woa.populationSize = 10
testWrap.woa.iterations = 500
testWrap1.fpa.populationSize = 20
testWrap1.fpa.iterations = 500
# n.createTrainData()
# nn.loadTrainingData()
# print(type(nn.TrainX))
# print(type(nn.TrainY))
#Qleran.setEpsilon(0.15)  # FPA needs higher epsilon
#fpa.iterations = 1500
#fpa.populationSize = 40
#for _ in range(5):
#    Qleran.createMap(4)
#    print("create done")
#    for strat in strats2:
#        Qleran.setStrategy(strat)
#        Qleran.learn()
#        print(Qleran.strategy.__class__)
#        print(Qleran.time)
#        print(Qleran.Qtime)
if True:
    nn.InputTrainNumber = 256 * 4
    nn.Qlearning.setStrategy(testWrap)
    nn.createTrainData("TrainingWrapWoa")
    nn.Qlearning.setStrategy(testWrap1)
    nn.createTrainData("TrainingWrapFpa")
    nn.setStrategy(None)
    nn.createTrainData("TrainingNormal")


# for population in range(10, 110, 10):
#    for iterations in range(100, 3100, 100):
#        woatime = []
#        woaQtime = []
#        fpatime = []
#        fpaQtime = []
#        for _ in range(20):
#            woa.iterations = iterations
#            woa.populationSize = population
#            fpa.iterations = iterations
#            fpa.populationSize = population
#            Qleran.createMap(4)
#            # Qleran.map.viewMap()
#            Qleran.setStrategy(woa)
#            Qleran.learn()
#            woatime.append(Qleran.time)
#            woaQtime.append(Qleran.Qtime)
#            Qleran.setStrategy(fpa)
#            Qleran.learn()
#            fpatime.append(Qleran.time)
#            fpaQtime.append(Qleran.Qtime)
#        print(f"Iterations {iterations}, population {population} \n")
#        print(f"woa avgt {avg(woatime)}, avgqt {avg(woaQtime)} \n")
#        print(f"fpa avgt {avg(fpatime)}, avgqt {avg(fpaQtime)} \n")

# Qleran.plotPath()
# prt(Qleran.steps)
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
