import math
import rospy
import matplotlib.pyplot as plt
import gazeboCommunication as gzlib
import Mapa as mp
import Qlearning as Q
import FPA as f
def avg(lst):
    return sum(lst) / len(lst)
fpa=f.FPA()
l=Q.Qlearning()
l.createMap(2)
l.setEpsilon(0.01)
times=[]
for i in range(10):
    l.learn()
    times.append(l.time)
print (avg(times))
l.setEpsilon(0.01)
l.setStrategy(fpa)
for i in range(10):
    l.learn()
    times[i]=l.time
print (avg(times))
l.createMap(1)
l.setEpsilon(0.01)
l.resetStrategy()
for i in range(10):
    l.learn()
    times[i]=l.time
print (avg(times))
l.setEpsilon(0.01)
l.setStrategy(fpa)
for i in range(10):
    l.learn()
    times[i]=l.time   
print (avg(times)) 

