#!/usr/bin/env python
import numpy as np
import math
import gazeboCommunication as gzlib
import Mapa as mp
import random
import matplotlib.pyplot as plt
import time
class Qlearning:
    def __init__(self):
        self.map=mp.Map()
        self.map.createMap()
        self.map.createCMap()
        self.gazebo=0
        self.epsilon=0
        self.alpha=0.2
        self.gamma=0.8
        self.time=0
        self.strategyFlag=False
    def createMap(self,type):
        self.map.createMap(type)
        self.map.createCMap()
        if self.gazebo:
            self.map.createGazeboMap()
    def setMap(self,map):
        self.map=map
    def getMap(self):
        return self.map
    def setEpsilon(self,epsilon):
        self.epsilon=epsilon
    def setAlpha(self,alpha):
        self.alpha=alpha
    def setGamma(self,gamma):
        self.gamma=gamma
    def setStrategy(self,strategy):
        self.strategyFlag=True
        self.strategy=strategy
    def resetStrategy(self):
        self.strategyFlag=False
    def initializeQMatrix(self):
        if self.strategyFlag==0:
            self.Q=np.zeros((self.map.size[0]*self.map.size[1],4))
        else:
            self.Q=self.strategy.initialize(self.map,self.gazebo)
    def learn(self):
        start=time.time()
        self.initializeQMatrix()
        self.steps=[]
        self.a=-1
        self.nextState=()
        self.r=0
        temp_eps=self.epsilon
        for i in range(100):
            self.state=self.map.startingPoint
            stepNr=0
            self.epsilon=temp_eps*(1-i/75)
            self.StartPioneer()
            while self.state != self.map.target:
                self.NextAction()
                self.Reinforcment()
                self.UpdateQ()
                self.state=self.nextState
                stepNr+=1
            self.steps.append(stepNr)
            self.DealWithPioneer()
        self.epsilon=temp_eps
        self.time=(time.time()-start)
    def NextAction(self):
        epsilon=random.random()
        Q=[]
        if epsilon<self.epsilon:
            self.a=random.randint(0,3)
        else:
            PossibleStates=[]
            PossibleStates.append((self.state[0]-1,self.state[1]))
            PossibleStates.append((self.state[0]+1,self.state[1]))
            PossibleStates.append((self.state[0],self.state[1]-1))
            PossibleStates.append((self.state[0],self.state[1]+1))
            for posState in PossibleStates:
                if posState[0]<=0 or posState[1] <= 0 or posState[0]>= self.map.size[0] or posState[1] >= self.map.size[1]:
                    Q.append(-100)
                elif posState==self.map.target:
                    Q.append(200)
                else:
                    val=max(self.Q[posState[0]+(posState[1]-1)*20-1])
                    Q.append(val)
            indexes=[]
            max_value = max(Q)
            for i in range(len(Q)):
                if Q[i]==max_value:
                    indexes.append(i)
            self.a=random.choice(indexes)




    def Reinforcment(self):
        if self.gazebo:
            self.ReinforceGazebo()
        else:
            self.ReinforceSim()
        
    def ReinforceSim(self):
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
        pos=self.state[0]+(self.state[1]-1)*20 -1
        self.Q[pos][self.a]=(1-self.alpha)*self.Q[pos][self.a]+self.alpha*(self.r+self.gamma*max(self.Q[self.nextState[0]+(self.nextState[1]-1)*20 -1]))
    def StartPioneer(self):
        if self.gazebo:
            gz=gzlib.GazeboCommunication()
            gz.spawnPioneer(self.map.startingPoint[0],self.map.startingPoint[1])
    def DealWithPioneer(self):
        if self.gazebo:
            gz=gzlib.GazeboCommunication()
            gz.deleteModel("Pioneer2DX")
    def plotSteps(self,show=True,fig=-1):
        if fig==-1:
            fig, ax = plt.subplots(figsize=(6, 6))
        else:
            plt.figure(fig.number)
        plt.plot(self.steps)
        if(show):
            plt.show()
        return fig
    def plotPath(self,show=True,fig=-1):
        return self.map.plotPath(self.Q,show,fig)
        


