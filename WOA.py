import numpy as np
import random
import math
from interfaces import InitializationInterface
import Qlearning as Q
class WOA(InitializationInterface):
    def __init__(self):
        self.iterations=500
        self.Reinfocment=Q.Qlearning()
        self.Reinfocment.initializeQMatrix()
        self.b=0
        self.initA=2
        self.probability=0.5
        self.populationSize=30
    def initialize(self,map,gazebo):
        self.map=map
        self.gazebo=gazebo
        self.Q=np.zeros((self.map.size[0]*self.map.size[1],4))
        self.Reinfocment.setMap(map)
        self.Reinfocment.gazebo=gazebo
        population=self.initialPopulation()
        a=np.array([self.initA,self.initA])
        bestFitness=0
        nextPopulation=[]
        fitnessList=[]
        for i in range(self.populationSize):
            nextPopulation.append(0)
            fitnessList.append(self.fitness(population[i]))
        for j in range(self.iterations):
            a=self.initA*(1-j/self.iterations)
            tempBest=max(fitnessList)
            index=fitnessList.index(tempBest)
            for i in range(self.populationSize):
                Agent=population[i]
                ra=np.array([random.random(),random.random()])
                rc=np.array([random.random(),random.random()])
                A=2*a*ra-a
                C=2*rc
                p=random.random()
                l=random.random()*(2)-1
                if p<self.probability:
                    if np.linalg.norm(A)<1:
                        G=population[index]
                        D=(C*G-Agent)
                        nextPopulation[i]=G-A*D
                        
                    else:
                        k=int(random.random()*(self.populationSize-1))
                        G=population[k]
                        D=(C*G-Agent)
                        nextPopulation[i]=G-A*D
                        
                else:
                    G=population[index]
                    D=(G-Agent)
                    nextPopulation[i]=D*math.exp(self.b*l)*math.cos(2*math.pi*l)+G
                    
                nextPopulation[i]=nextPopulation[i].round().astype(int)
                if nextPopulation[i][0]<0:
                    nextPopulation[i][0]=0
                elif nextPopulation[i][0]>= self.map.size[1]:
                    nextPopulation[i][0]=20
                if nextPopulation[i][1]<0:
                    nextPopulation[i][1]=0
                elif nextPopulation[i][1]>= self.map.size[1]:
                    nextPopulation[i][1]=20
                #nextPopulation[i][nextPopulation[i]>=self.map.size[1]]=self.map.size[1]-1
                #nextPopulation[i][nextPopulation[i]<0]=0
                fitnessList[i]=self.fitness(nextPopulation[i])
        #print("woa")
        return self.Reinfocment.Q
    def fitness(self,Whale):
        self.Reinfocment.state=Whale
        for i in range(4):
            self.Reinfocment.a=i
            self.Reinfocment.Reinforcment()
            self.Reinfocment.UpdateQ()
        return max(self.Reinfocment.Q[Whale[0]+Whale[1]*20 -21])

    def initialPopulation(self):
        population=[]
        for i in range(self.populationSize):
            #x=random.randint(1,self.map.size[0])
            #y=random.randint(1,self.map.size[1])
            x=int(random.random()*(self.map.size[0]-1)+1)
            y=int(random.random()*(self.map.size[1]-1)+1)
            while self.map.checkInterior(x,y):
                x=int(random.random()*(self.map.size[0]-1)+1)
                y=int(random.random()*(self.map.size[1]-1)+1)
                #x=random.randint(1,self.map.size[0])
                #y=random.randint(1,self.map.size[1])
            population.append(np.array([x,y]))
        return population