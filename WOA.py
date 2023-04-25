import numpy as np
import random
import math
from interfaces import InitializationInterface
import Qlearning as Q


class WOA(InitializationInterface):
    def __init__(self):
        self.iterations = 500
        self.b = 0
        self.initA = 2
        self.probability = 0.5
        self.populationSize = 30
        self.gamma = 0.5
        self.updateAlpha = 0.2

    def initialize(self, map, gazebo):
        self.map = map
        self.gazebo = gazebo
        self.Q = np.zeros((self.map.size[0], self.map.size[1], 4))
        population = self.initialPopulation()
        a = np.array([self.initA, self.initA])
        bestFitness = 0
        nextPopulation = []
        fitnessList = []
        for i in range(self.populationSize):
            nextPopulation.append(0)
            fitnessList.append(self.fitness(population[i]))
        for j in range(self.iterations):
            a = self.initA * (1 - j / self.iterations)
            tempBest = max(fitnessList)
            index = fitnessList.index(tempBest)
            for i in range(self.populationSize):
                Agent = population[i]
                ra = np.array([random.random(), random.random()])
                rc = np.array([random.random(), random.random()])
                A = 2 * a * ra - a
                C = 2 * rc
                p = random.random()
                l = random.random() * (2) - 1
                if p < self.probability:
                    if np.linalg.norm(A) < 1:
                        G = population[index]
                        D = C * G - Agent
                        nextPopulation[i] = G - A * D

                    else:
                        k = int(random.random() * (self.populationSize - 1))
                        G = population[k]
                        D = C * G - Agent
                        nextPopulation[i] = G - A * D

                else:
                    G = population[index]
                    D = G - Agent
                    nextPopulation[i] = (
                        D * math.exp(self.b * l) * math.cos(2 * math.pi * l) + G
                    )

                nextPopulation[i] = nextPopulation[i].round().astype(int)
                if nextPopulation[i][0] < 0:
                    nextPopulation[i][0] = 0
                elif nextPopulation[i][0] >= self.map.size[0]:
                    nextPopulation[i][0] = self.map.size[0] - 1
                if nextPopulation[i][1] < 0:
                    nextPopulation[i][1] = 0
                elif nextPopulation[i][1] >= self.map.size[1]:
                    nextPopulation[i][1] = self.map.size[1] - 1
                # nextPopulation[i][nextPopulation[i]>=self.map.size[1]]=self.map.size[1]-1
                # nextPopulation[i][nextPopulation[i]<0]=0
                fitnessList[i] = self.fitness(nextPopulation[i])
        # print("woa")
        return self.Q.copy()

    def fitness(self, whale):
        self.state = whale
        for i in range(4):
            self.a = i
            self.Reinforcment()
            self.UpdateQ()
        return max(self.Q[self.state[0]][self.state[1]])

    def Reinforcment(self):
        if self.gazebo:
            self.ReinforceGazebo()
        else:
            self.ReinforceSim()

    def ReinforceSim(self):
        if self.map.checkInterior(self.state[0], self.state[1]):
            self.r = -10
            self.nextState = self.state
            return
        if self.a == 0:
            posNext = (self.state[0] - 1, self.state[1])
        elif self.a == 1:
            posNext = (self.state[0] + 1, self.state[1])
        elif self.a == 2:
            posNext = (self.state[0], self.state[1] - 1)
        else:
            posNext = (self.state[0], self.state[1] + 1)
        if (
            posNext[0] <= 0
            or posNext[0] >= self.map.size[0]
            or posNext[1] <= 0
            or posNext[1] >= self.map.size[1]
        ):
            self.r = -1
            self.nextState = self.state
            return
        if self.map.checkInterior(posNext[0], posNext[1]):
            self.r = -1
            self.nextState = self.state
            return
        if posNext == self.map.target:
            self.r = 2
            self.nextState = posNext
            return
        self.r = 0
        self.nextState = posNext

    def ReinforceGazebo(self):
        pass

    def UpdateQ(self):
        self.Q[self.state[0]][self.state[1]][self.a] = (1 - self.updateAlpha) * self.Q[
            self.state[0]
        ][self.state[1]][self.a] + self.updateAlpha * (
            self.r + self.gamma * max(self.Q[self.nextState[0]][self.nextState[1]])
        )

    def initialPopulation(self):
        population = []
        for i in range(self.populationSize):
            # x=random.randint(1,self.map.size[0])
            # y=random.randint(1,self.map.size[1])
            x = int(random.random() * (self.map.size[0]))
            y = int(random.random() * (self.map.size[1]))
            while self.map.checkInterior(x, y):
                x = int(random.random() * (self.map.size[0]))
                y = int(random.random() * (self.map.size[1]))
                # x=random.randint(1,self.map.size[0])
                # y=random.randint(1,self.map.size[1])
            population.append(np.array([x, y]))
        return population

    def save(self, path="data.txt", full=True, Q=True):
        with open(path, "a") as file:
            file.write(f"{__name__}: \n")
            if full:
                file.write(f"i {self.iterations} \n")
                file.write(f"b {self.b} \n")
                file.write(f"iA {self.initA} \n")
                file.write(f"pb {self.probability} \n")
                file.write(f"ps {self.populationSize} \n")
            if Q:
                file.write(f"Qi {np.array_str(self.Q)} \n")
