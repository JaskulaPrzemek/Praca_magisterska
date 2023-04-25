import numpy as np
import random
import math
from interfaces import InitializationInterface
import Qlearning as Q
import matplotlib.pyplot as plt


class APF(InitializationInterface):
    def __init__(self):
        self.attractivePot = True
        self.repulsivePot = False
        self.atractScale = 3.1
        self.repulseScale = -0.00006
        self.influenceDistance = 2
        self.inverseInfuence = 1 / self.influenceDistance
        self.Umax = 0.5

    def setAttractivePot(self):
        self.attractivePot = True

    def resetAttractivePot(self):
        self.attractivePot = False

    def setRepulsivePot(self):
        self.repulsivePot = True

    def resetRepulsivePot(self):
        self.repulsivePot = False

    def setAttractScale(self, scale):
        self.atractScale = scale

    def setRepulseScale(self, scale):
        self.repulseScale = scale

    def setUmax(self, Um):
        self.Umax = Um

    def setInfuenceDistance(self, dist):
        self.influenceDistance = dist

    def getAttract(self):
        return self.test

    def getQMatrix(self):
        return self.Q

    def initialize(self, map, gazebo):
        self.map = map
        self.size = map.size
        target = map.target
        self.Q = np.zeros((self.map.size[0], self.map.size[1], 4))
        self.test = np.zeros((self.map.size[0], self.map.size[1]))
        aPot = 0
        aRep = 0
        for i in range(map.size[0]):
            for j in range(map.size[1]):
                point = (i, j)
                if self.attractivePot:
                    # aPot=0.5*self.atractScale*(self.distance(point,target)**2)
                    aPot = self.atractScale * math.exp(
                        -0.5 * ((i - target[0]) ** 2 + (j - target[1]) ** 2)
                    )
                else:
                    aPot = 0
                if self.repulsivePot:
                    aRep = 0
                    for obstacle in self.map.obstacles:
                        midpoint = self.midpoint(obstacle)
                        distance = self.distance(point, midpoint)
                        if distance < self.influenceDistance:
                            aRep = (
                                aRep
                                + 0.5
                                * self.repulseScale
                                * (1 / distance - self.inverseInfuence) ** 2
                            )
                            if aRep < -1:
                                aRep = -1
                U = (self.Umax - aPot - aRep) / self.Umax
                self.Q[i][j] = aPot - aRep
                self.test[j][i] = aPot + aRep
        self.test[self.test == -1] = min(self.test[self.test > -1])

        # print("apf")
        return self.Q.copy()

    def showAttract(self):
        plt.imshow(self.test)
        plt.xlim([0, self.size[0]])
        plt.ylim([0, self.size[1]])
        plt.xticks(np.arange(0, self.size[0], 2))
        plt.yticks(np.arange(0, self.size[1], 2))
        plt.show()

    def distance(self, point1, point2):
        diff1 = (point1[0] - point2[0]) ** 2
        diff2 = (point1[1] - point2[1]) ** 2
        return math.sqrt(diff1 + diff2)

    def midpoint(self, obstacle):
        # could be moved to map and be even faste?
        area = 0
        sumx = 0
        sumy = 0
        for i in range(len(obstacle) - 1):
            obs = obstacle[i]
            obs1 = obstacle[i + 1]
            diff = obs[0] * obs1[1] - obs1[0] * obs[1]
            sumx = sumx + (obs[0] + obs1[0]) * diff
            sumy = sumy + (obs[1] + obs1[1]) * diff
            area = area + diff
        area = area * 3
        x = sumx / area
        y = sumy / area
        return (x, y)

    def save(self, path="data.txt", full=True, Q=True):
        with open(path, "a") as file:
            file.write(f"{__name__}: \n")
            if full:
                if self.attractivePot:
                    file.write(f"as {self.atractScale}: \n")
                if self.repulsivePot:
                    file.write(f"rs {self.repulseScale}: \n")
                file.write(f"D {self.influenceDistance}: \n")
            if Q:
                file.write(f"Q {np.array_str(self.Q)} \n")
