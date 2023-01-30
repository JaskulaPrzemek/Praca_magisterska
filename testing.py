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
def avg(lst):
    return sum(lst) / len(lst)
show=False
fpa=f.FPA()
l=Q.Qlearning()
apf=a.APF()
woa=w.WOA()
l.createMap(2)
#l.map.viewMap()
l.setEpsilon(0.01)
times=[]
l.learn()
print(l.time)
#path=l.plotPath(show)
#steps=l.plotSteps(show)
l.setStrategy(fpa)
l.learn()
print(l.time)
l.setEpsilon(0.01)
l.setStrategy(woa)
l.learn()
print(l.time)
print(l.Qtime)
#path=l.plotPath(show)
#steps=l.plotSteps(show)
l.setStrategy(apf)
l.learn()
print(l.time)
#plt.show()
#apf.showAttract()
#l.plotPath(show,path)
#l.plotSteps(show,steps)
#plt.show()
