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
import math

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
 
class linia:
    R=0.0
    def __init__(self, p11, p12, p21, p22):
        self.p1=[p11,p12]
        self.p2=[p21,p22]
    def calcR(self):
        px=self.p1[0]-self.p2[0]
        py=self.p1[1]-self.p2[1]
        self.R=px*px+py*py
        return self.R
        

def find_points(linePoints):
    linie=[]
    for i in range(len(linePoints)):
        linie.append(linia(linePoints[i][0][0],linePoints[i][0][1],linePoints[i][1][0],linePoints[i][1][1]))
        linie[i].calcR()
    maxR1=max(linie, key=lambda item: item.R)
    linie.remove(maxR1)
    maxR2=max(linie, key=lambda item: item.R)
    #print(maxR1.p1)
    #print(maxR1.p2)
    maxD=-100
    tempd=calcOdleglosc(maxR1.p1,maxR2.p1)
    if(tempd>maxD):
        p1=maxR1.p1
        p2=maxR2.p1
        maxD=tempd
    tempd=calcOdleglosc(maxR1.p1,maxR2.p2)
    if(tempd>maxD):
        p1=maxR1.p1
        p2=maxR2.p2
        maxD=tempd
    tempd=calcOdleglosc(maxR1.p2,maxR2.p1)
    if(tempd>maxD):
        p1=maxR1.p2
        p2=maxR2.p1
        maxD=tempd
    tempd=calcOdleglosc(maxR1.p2,maxR2.p2)
    if(tempd>maxD):
        p1=maxR1.p2
        p2=maxR2.p2
        maxD=tempd
    p3=line_intersection([maxR1.p1,maxR1.p2],[maxR2.p1,maxR2.p2])
    return [p1, p2, p3]
    

def calcOdleglosc(p1, p2):
    px=p1[0]-p2[0]
    py=p1[1]-p2[1]
    return px*px+py*py

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return [x, y]

def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang


x = np.arange(0,512)
theta = (np.pi/512 )*(x-256)  # kat w radianach

# Wczytanie skanu z pierwszego zestawu danych
skan=data[4]["scan"]
limit=2
x=line_detection(skan,180,limit)
lc1 = mc.LineCollection(x, colors=[0,0,0],linewidths=1)
fig, ax = pl.subplots()
ax.add_collection(lc1)
ax.autoscale()
fig1 = plt.figure()
ax1 = fig1.add_axes([0.1,0.1,0.8,0.8],polar=True)
line, = ax1.plot(theta,skan,lw=2.5)
ax1.set_ylim(0,4)  # zakres odleglosci
y=find_points(x)
print(getAngle([1,1],[0,0],y[1]))
print(getAngle([1,1],[0,0],y[0]))
print(getAngle([1,1],[0,0],y[2]))
print(10.898437500000007-getAngle([1,1],[0,0],y[1]))
plt.show()