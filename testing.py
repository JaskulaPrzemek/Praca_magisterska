import math
import rospy
import matplotlib.pyplot as plt
import gazeboCommunication as gzlib
import Mapa as mp
import Qlearning as Q
import FPA as f
import APF as a
import WOA as w
import random
import time
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
times=[]
for i in range(10):
    start=time.time()
    l.createMap(3) 
    l.learn()
    times.append(time.time()-start)
    #path=l.plotPath(show)
    #steps=l.plotSteps(show)
print(max(times))
print(avg(times))
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
