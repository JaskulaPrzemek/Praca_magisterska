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
fpa=f.FPA()

l=Q.Qlearning()
l.createMap(2)
l.setStrategy(fpa)
l.setEpsilon(0.01)
times=[]
compute_time=[]
for i in range(10):
    l.learn()
    times.append(l.time)

print("avg")
print(avg(times))
l.createMap(1)
for i in range(10):
    l.learn()
    times[i]=(l.time)
print("avg")
print(avg(times))
l.createMap(2)
l.resetStrategy()
l.setEpsilon(0)
for i in range(10):
    l.learn()
    times[i]=(l.time)
print("avg")
print(avg(times))
l.createMap(1)
for i in range(10):
    l.learn()
    times[i]=(l.time)
print("avg")
print(avg(times))
