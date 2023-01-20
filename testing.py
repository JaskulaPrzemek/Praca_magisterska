import math
import rospy
import matplotlib.pyplot as plt
import gazeboCommunication as gzlib
import Mapa as mp
import Qlearning as Q
import FPA as f
import random
def avg(lst):
    return sum(lst) / len(lst)
show=False
fpa=f.FPA()
l=Q.Qlearning()
l.createMap(2)
l.setEpsilon(0.01)
times=[]
l.learn()
print(l.time)
path=l.plotPath(show)
steps=l.plotSteps(show)
l.setStrategy(fpa)
l.learn()
print(l.time)
l.plotPath(show,path)
l.plotSteps(show,steps)
plt.show()
