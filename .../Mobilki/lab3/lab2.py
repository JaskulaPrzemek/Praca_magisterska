import json
##wczytanie danych z pliku
json_data = open('line_localization_1.json')
data = json.load(json_data)

### wykres danych ze skanera w ukladzie biegunowym
import matplotlib.pyplot as plt
import numpy as np
from math import hypot, pi, cos, sin,isinf,tan
from matplotlib import collections  as mc
import pylab as pl

def line_detection(json,n,limit):
    x = np.arange(0,512)
    theta = (np.pi/512 )*(x-256) 
    points=[]
    linePoints=[]
    for i in range(len(json)):
        if(not isinf(json[i])):
            if(json[i]<limit):
                points.append((json[i],theta[i]))
    step=np.pi/(n+2)
    thetaList=np.arange(step-np.pi,np.pi-step,step)
    sinlist=np.sin(thetaList)
    coslist=np.cos(thetaList)
    pointList=[]
    array=np.zeros((n,len(points)))
    j=0
    for point in points:
        x=point[0]*cos(point[1])
        y=point[0]*sin(point[1])
        pointList.append((x,y))
        for i in range(n):
            array[i][j]=round(x*coslist[i]+y*sinlist[i],2)
        j=j+1
    while True:
        countList=[]
        if(len(array[0])<2):
            return linePoints
        for i in range(n):
            values, counts = np.unique(array[i], return_counts=True)
            ind = np.argmax(counts)
            countList.append((values[ind],counts[ind]))
        mostcommon=max(countList,key=lambda item:item[1])
        if(mostcommon[1]<5):
            break
        maxindex=countList.index(mostcommon)
        allindexes=np.where((array[maxindex]>mostcommon[0]-0.04 )& (array[maxindex]<mostcommon[0]+0.04 ))
        linePoints.append([pointList[allindexes[0][0]],pointList[allindexes[0][len(allindexes[0])-1]]])
        array=np.delete(array,allindexes[0],1)
        for i in sorted(allindexes[0], reverse=True):
            del pointList[i]
    return linePoints
 




x = np.arange(0,512)
theta = (np.pi/512 )*(x-256)  # kat w radianach

# Wczytanie skanu z pierwszego zestawu danych
skan=data[2]["scan"]
limit=1.5
x=line_detection(skan,80,limit)
lc1 = mc.LineCollection(x, colors=[0,0,0],linewidths=1)
fig, ax = pl.subplots()
ax.add_collection(lc1)
ax.autoscale()
fig1 = plt.figure()
ax1 = fig1.add_axes([0.1,0.1,0.8,0.8],polar=True)
line, = ax1.plot(theta,skan,lw=2.5)
ax1.set_ylim(0,4)  # zakres odleglosci
plt.show()

