import math
try:
    import rospy
    import gazeboCommunication as gzlib
except(ImportError):
    pass
import matplotlib.pyplot as plt

import Mapa as mp
import Qlearning as Q
import FPA as f
import APF as a
import WOA as w
import random
import time
import numpy as np
def avg(lst):
    return sum(lst) / len(lst)
show=False
fpa=f.FPA()
l=Q.Qlearning()
apf=a.APF()
woa=w.WOA()
l.createMap(3)
#l.map.viewMap()
l.setEpsilon(0.01)
l.setStrategy(woa)
times=[]
lenght=[]
smoothness=[]
path="data1.txt"
l.createMap(3) 
#l.map.save(path)
for i in range(1):
    l.learn()
    times.append(l.time)
    lenght.append(l.pathLenght)
    smoothness.append(l.pathSmoothness)
    #path=l.plotPath(show)
    #steps=l.plotSteps(show)
    #l.save(path,mapa=False,strategy=True,sFull=True,Q=True,sQ=True)
    #l.plotPath()
    
print(max(times))
print(avg(times))
print(max(lenght))
print(avg(lenght))
print(max(smoothness))
print(avg(smoothness))


#l.setStrategy(fpa)
#l.learn()
#print(l.time)
#l.setEpsilon(0.01)
#l.setStrategy(woa)
#l.learn()
#print(l.time)
#print(l.Qtime)
#path=l.plotPath(show)
#steps=l.plotSteps(show)
#l.setStrategy(apf)
#l.learn()
#print(l.time)
#plt.show()
#apf.showAttract()
#l.plotPath(show,path)
#l.plotSteps(show,steps)
#plt.show()