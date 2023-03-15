import numpy as np
import random
import math
from interfaces import InitializationInterface
class FPA(InitializationInterface):
    def __init__(self):
        self.gamma=0.5
        self.iterations=100
        self.updateGamma=0.8
        self.updateAlpha=0.2
        self.populationSize=10
        self.gazebo=False
        self.probability=0.5
        self.beta=1.4
        self.num=math.gamma(self.beta)*math.sin(math.pi*self.beta/2)
        self.den=math.gamma((1+self.beta)/2)*self.beta*(2**(self.beta-1)/2)
        self.sigma_u=(self.num/self.den)**(1/self.beta)
    def setBeta(self,beta):
        self.beta=beta
        self.num=math.gamma(self.beta)*math.sin(math.pi*self.beta/2)
        self.den=math.gamma((1+self.beta)/2)*self.beta*(2**(self.beta-1)/2)
        self.sigma_u=(self.num/self.den)**(1/self.beta)
    def setGamma(self,gamma):
        self.gamma=gamma
    def setIterations(self,iterations):
        self.iterations=iterations
    def setUpdateGamma(self,gamma):
        self.updateGamma=gamma
    def setUpdateAlpha(self,alpha):
        self.updateAlpha=alpha
    def setPopulationSize(self,popSize):
        self.populationSize=popSize
    def setProbability(self,prob):
        self.probability=prob
    def initialize(self,map,gazebo):
        self.map=map
        self.gazebo=gazebo
        self.Q=np.zeros((self.map.size[0]*self.map.size[1],4))
        population=self.initialPopulation()
        bestFitness=0
        nextPopulation=[]
        fitnessList=[]
        for i in range(self.populationSize):
            nextPopulation.append(0)
            fitnessList.append(self.fitness(population[i]))
        for j in range(self.iterations):
            tempBest=max(fitnessList)
            index=fitnessList.index(tempBest)
            if tempBest>=bestFitness:
                bestFitness=tempBest
                bestFlower=population[index]
            for i in range(self.populationSize):
                temp=np.array([0,0])
                while temp[0]<1 or temp[0]>= self.map.size[0] or temp[1]<1 or temp[1]>= self.map.size[1]:
                    if(random.random()>self.probability):
                        temp=population[i]+self.gamma*self.levy()*(population[i]-bestFlower)
                    else:
                        #j=random.randint(0,self.populationSize-1)
                        #k=random.randint(0,self.populationSize-1)
                        j=int(random.random()*(self.populationSize))
                        k=int(random.random()*(self.populationSize))
                        temp=population[i]+random.random()*(population[j]-population[k])
                temp=temp.round().astype(int)
                fitness=self.fitness(temp)
                if fitness>fitnessList[i]:
                    nextPopulation[i]=temp
                else:
                    nextPopulation[i]=population[i]
            population=nextPopulation
        return self.Q.copy()
    def fitness(self,flower):
        self.state=flower
        for i in range(4):
            self.a=i
            self.Reinforcment()
            self.UpdateQ()
        return max(self.Q[self.state[0]+self.state[1]*20 -21])
    def Reinforcment(self):
        if self.gazebo:
            self.ReinforceGazebo()
        else:
            self.ReinforceSim()
        
    def ReinforceSim(self):
        if self.map.checkInterior(self.state[0],self.state[1]):
            self.r =-10
            self.nextState=self.state
            return
        if self.a==0:
            posNext=(self.state[0]-1,self.state[1])
        elif self.a==1:
            posNext=(self.state[0]+1,self.state[1])
        elif self.a==2:
            posNext=(self.state[0],self.state[1]-1)
        else:
            posNext=(self.state[0],self.state[1]+1)
        if posNext[0]<=0 or posNext[0]>= self.map.size[0] or posNext[1]<=0 or posNext[1]>= self.map.size[1]:
            self.r=-1
            self.nextState=self.state
            return
        if self.map.checkInterior(posNext[0],posNext[1]):
            self.r=-1
            self.nextState=self.state
            return
        if posNext== self.map.target:
            self.r=2
            self.nextState=posNext
            return
        self.r=0
        self.nextState=posNext

    def ReinforceGazebo(self):
        pass
    def UpdateQ(self):
        pos=self.state[0]+self.state[1]*20 -21
        self.Q[pos][self.a]=(1-self.updateAlpha)*self.Q[pos][self.a]+self.updateAlpha*(self.r+self.gamma*max(self.Q[self.nextState[0]+self.nextState[1]*20 -21]))
        
    def levy(self):
        u=np.random.normal(0,self.sigma_u**2,2)
        v=np.random.normal(0,1,2)
        return u/(abs(v)**(1/self.beta))

    def initialPopulation(self):
        population=[]
        for i in range(self.populationSize):
            #x=random.randint(1,self.map.size[0])
            #y=random.randint(1,self.map.size[1])
            x=int(random.random()*(self.map.size[0])+1)
            y=int(random.random()*(self.map.size[1])+1)
            while self.map.checkInterior(x,y):
                x=int(random.random()*(self.map.size[0])+1)
                y=int(random.random()*(self.map.size[1])+1)
                #x=random.randint(1,self.map.size[0])
                #y=random.randint(1,self.map.size[1])
            population.append(np.array([x,y]))
        return population
    def save(self,path="data.txt",full=True,Q=True):
        with open(path, "a") as file:
            file.write( f"{__name__}: \n" )
            if full:
                file.write( f"g {self.gamma} \n")
                file.write( f"i {self.iterations} \n")
                file.write( f"ug {self.updateGamma} \n")
                file.write( f"ua {self.updateAlpha} \n")
                file.write( f"ps {self.populationSize} \n")
                file.write( f"p {self.probability} \n")
                file.write( f"b {self.beta} \n")
            if Q:
                file.write( f"Q {np.array_str(self.Q)} \n")