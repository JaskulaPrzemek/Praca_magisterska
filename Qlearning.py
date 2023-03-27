#!/usr/bin/env python
import numpy as np
import math
import gazeboCommunication as gzlib
import Mapa as mp
import random
import matplotlib.pyplot as plt
import time
import sys


class Qlearning:
    def __init__(self):
        self.map = mp.Map()
        self.map.createMap()
        self.map.createCMap()
        self.gazebo = 0
        self.epsilon = 0
        self.alpha = 0.2
        self.gamma = 0.8
        self.time = 0
        self.strategyFlag = False
        self.disableInit = False
        np.set_printoptions(threshold=sys.maxsize, suppress=True)

    def createMap(self, type):
        self.map.createMap(type)
        self.map.createCMap()
        if self.gazebo:
            self.map.createGazeboMap()

    def setMap(self, map):
        self.map = map

    def getMap(self):
        return self.map

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def setAlpha(self, alpha):
        self.alpha = alpha

    def setGamma(self, gamma):
        self.gamma = gamma

    def setDisableInit(self):
        self.disableInit = True

    def reSetDisableInit(self):
        self.disableInit = False

    def setStrategy(self, strategy):
        self.strategyFlag = True
        self.strategy = strategy

    def resetStrategy(self):
        self.strategyFlag = False
        self.strategy = None

    def initializeQMatrix(self):
        if self.strategyFlag == 0:
            self.Q = np.zeros((self.map.size[0] * self.map.size[1], 4))
        else:
            self.Q = self.strategy.initialize(self.map, self.gazebo)

    def learn(self):
        start = time.time()
        if not self.disableInit:
            self.initializeQMatrix()
        self.Qtime = time.time() - start
        self.steps = []
        self.a = -1
        self.nextState = ()
        self.r = 0
        temp_eps = self.epsilon
        flag = False
        for i in range(100):
            self.state = self.map.startingPoint
            stepNr = 0
            self.epsilon = temp_eps * (1 - i / 75)
            self.StartPioneer()
            pp = []
            while self.state != self.map.target:
                pp.append(self.state)
                self.NextAction()
                self.Reinforcment()
                self.UpdateQ()
                self.state = self.nextState
                stepNr += 1
                # print(self.state)
                # print(stepNr)
                if stepNr > 100000:
                    # print(stepNr)
                    flag = True
                    break
            if flag:
                self.Q = np.zeros((self.map.size[0] * self.map.size[1], 4))
                self.steps.append(stepNr)
                break
            # print(stepNr)
            self.steps.append(stepNr)
            self.DealWithPioneer()
        self.epsilon = temp_eps
        self.time = time.time() - start
        if not self.disableInit:
            self.getPath(flag)

    def NextAction(self):
        epsilon = random.random()
        Q = []
        if epsilon < self.epsilon:
            # self.a = random.randint(0, 3)
            self.a = int(random.random() * (4))
        else:
            PossibleStates = [
                (self.state[0] - 1, self.state[1]),
                (self.state[0] + 1, self.state[1]),
                (self.state[0], self.state[1] - 1),
                (self.state[0], self.state[1] + 1),
            ]

            for x, y in PossibleStates:
                if x <= 0 or y <= 0 or x >= self.map.size[0] or y >= self.map.size[1]:
                    Q.append(-100)
                elif (x, y) == self.map.target:
                    Q.append(200)
                else:
                    val = max(self.Q[x + (y - 1) * 20 - 1])
                    Q.append(val)
            indexes = []
            max_value = max(Q)
            for index, value in enumerate(Q):
                if value == max_value:
                    indexes.append(index)
            if len(indexes) == 1:
                self.a = indexes[0]
            else:
                i = int(random.random() * (len(indexes)))
                self.a = indexes[i]

    def Reinforcment(self):
        if self.gazebo:
            self.ReinforceGazebo()
        else:
            self.ReinforceSim()

    def ReinforceSim(self):
        if self.a == 0:
            x, y = (self.state[0] - 1, self.state[1])
        elif self.a == 1:
            x, y = (self.state[0] + 1, self.state[1])
        elif self.a == 2:
            x, y = (self.state[0], self.state[1] - 1)
        else:
            x, y = (self.state[0], self.state[1] + 1)
        if (
            x <= 0
            or x >= self.map.size[0]
            or y <= 0
            or y >= self.map.size[1]
            or self.map.checkInterior(x, y)
        ):
            self.r = -1
            self.nextState = self.state
            return
        if (x, y) == self.map.target:
            self.r = 2
            self.nextState = (x, y)
            return
        self.r = 0
        self.nextState = (x, y)

    def ReinforceGazebo(self):
        if self.a == 0:
            posNext = (self.state[0] - 1, self.state[1])
        elif self.a == 1:
            posNext = (self.state[0] + 1, self.state[1])
        elif self.a == 2:
            posNext = (self.state[0], self.state[1] - 1)
        else:
            posNext = (self.state[0], self.state[1] + 1)
        gz = gzlib.GazeboCommunication()
        [r, posNext] = gz.goToPoint(posNext, self.map.target)
        self.r = r
        self.nextState = posNext

    def UpdateQ(self):
        pos = self.state[0] + (self.state[1] - 1) * 20 - 1
        self.Q[pos][self.a] = (1 - self.alpha) * self.Q[pos][self.a] + self.alpha * (
            self.r
            + self.gamma
            * max(self.Q[self.nextState[0] + (self.nextState[1] - 1) * 20 - 1])
        )

    def StartPioneer(self):
        if self.gazebo:
            gz = gzlib.GazeboCommunication()
            gz.spawnPioneer(self.map.startingPoint[0], self.map.startingPoint[1])

    def DealWithPioneer(self):
        if self.gazebo:
            gz = gzlib.GazeboCommunication()
            gz.deleteModel("Pioneer2DX")

    def plotSteps(self, show=True, fig=-1):
        if fig == -1:
            fig, ax = plt.subplots(figsize=(6, 6))
        else:
            plt.figure(fig.number)
        plt.plot(self.steps)
        if show:
            plt.show()
        return fig

    def plotPath(self, show=True, fig=-1):
        return self.map.plotPath(self.Q, show, fig)

    def getPath(self, flag):
        if not flag:
            self.map.getPath(self.Q)
            self.path = self.map.path
            self.pathLenght = self.map.pathLenght
            self.pathSmoothness = self.map.pathSmoothness
        else:
            print("yo")
            self.path = []
            self.pathLenght = 100
            self.pathSmoothness = 100

    def save(
        self, path="data.txt", mapa=True, strategy=True, sFull=True, Q=True, sQ=True
    ):
        with open(path, "a") as file:
            file.write("Qlearn: \n")
            file.write(f"E {self.epsilon} \n")
            file.write(f"a {self.alpha} \n")
            file.write(f"g {self.gamma} \n")
            file.write(f"t {self.time} \n")
            file.write(f"st {str(self.steps)} \n")
            file.write(f"Qt {self.Qtime} \n")
            file.write(f"p {self.path} \n")
            file.write(f"l {self.pathLenght} \n")
            file.write(f"s {self.pathSmoothness} \n")
            file.write(f"Q {np.array_str(self.Q)} \n")
        if mapa:
            self.map.save(path)
        if self.strategyFlag and strategy:
            self.strategy.save(path, sFull, sQ)
