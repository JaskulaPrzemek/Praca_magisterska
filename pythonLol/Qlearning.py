#!/usr/bin/env python
import numpy as np
import math
import gazeboCommunication as gzlib
import Mapa as mp

class Qlearning:
    def __init__(self):
        self.map=mp.Map()
        self.map.createCMap()
        self.gazebo=0
    def setMap(self,type):
        self.map.createMap(type)
        self.map.createCMap()
    def initializeQMatrix(self,type=0):
        if type==0:
            self.Q=np.zeros(self.map.size[0]*self.map.size[1],4)

