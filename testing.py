import math
from RandomInitialization import randomInit

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


# woa = w.WOA()
# apf = a.APF()
# fpa = f.FPA()
Qleran = Q.Qlearning()
Qlearn = Q.Qlearning()
# AdamNorm = n.NN()
# AdamF = n.NN()
# AdamW = n.NN()
# SqdNorm = n.NN()
# SqdF = n.NN()
# SqdW = n.NN()
# AdamNorm.load("NewTest/MseAdamNorm.keras")
# AdamF.load("NewTest/MseAdamWrapF.keras")
# AdamW.load("NewTest/MseAdamWrapW.keras")
# SqdNorm.load("NewTest/MseSqdNorm.keras")
# SqdF.load("NewTest/MseSqdWrapF.keras")
# SqdW.load("NewTest/MseSqdWrapW.keras")
# testWrap = weirdWrapper()
# testWrap1 = weirdWrapper()
# testWrap1.flag = True
# strats = [None, apf, fpa, woa, testWrap, testWrap1]
# strats1 = [testWrap, testWrap1]
# strats2 = [None, fpa]
# strats = [AdamNorm, AdamF, AdamW, SqdNorm, SqdF, SqdW]
randomI = randomInit()
randomI.gauss = True
randNorm = randomInit()
randNorm.gauss = False
randNorm.Min = -0.5
randNorm.Max = 0.5
strats = [None, randomI, randNorm]
# nn.InputTrainNumber = 16
# testWrap.woa.populationSize = 10
# testWrap.woa.iterations = 500
# testWrap1.fpa.populationSize = 20
# testWrap1.fpa.iterations = 500
# n.createTrainData()
# nn.loadTrainingData()
# print(type(nn.TrainX))
# print(type(nn.TrainY))
# Qleran.setEpsilon(0.15)  # FPA needs higher epsilon
# fpa.iterations = 1500
# fpa.populationSize = 40
Qlearn.maxvalue = 10
Qlearn.learn()
Qlearn.createMap(4)
if Qlearn.path and Qlearn.pathLenght != 100 and Qlearn.pathSmoothness != 100:
    print("nah,allgood")
# for _ in range(15):
#    Qleran.createMap(4)
#    print("create done")
#    Qleran.maxvalue = 100000000
#    for strat in strats:
#        Qleran.setStrategy(strat)
#        # print(strat.ModelName)
#        Qleran.learn()
#        print(Qleran.time)
#        print(Qleran.Qtime)
#        # Qleran.plotPath()
# if True:
#    nn.InputTrainNumber = 256 * 4
#    nn.Qlearning.setStrategy(None)
#    nn.createTrainData("TrainingNormal")


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
