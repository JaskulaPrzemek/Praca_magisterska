import numpy as np
import math
import rospy
import time
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import matplotlib as mpl
import matplotlib.pyplot as plt
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import json
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
##wczytanie danych z pliku
json_data = open('map_round.json')
data = json.load(json_data)

mapDim=[20,20]
resolution=0.5
pHit=0.95
pMiss=0.05
pFree=0.40
inverse_sensor_model=math.log(pHit/(1-pHit))
freePointConstant=math.log(pFree/(1-pFree))
Mapa=np.zeros([int(mapDim[0]/resolution),int(mapDim[1]/resolution)],dtype=float)
MapaProb=np.zeros([int(mapDim[0]/resolution),int(mapDim[1]/resolution)],dtype=float)
trueDim=len(Mapa)
nr=2
x = np.arange(0,512)
theta = (np.pi/512 )*(x-256) 
x_ros=0
y_ros=0
yaw_ros=0

def listener():
    rospy.init_node('grupa5_scan_subscriber', anonymous=True)
    rospy.Subscriber('/PIONIER'+str(nr)+'/RosAria/pose', Odometry, callback_pose)
    time.sleep(1)
    rospy.Subscriber("/PIONIER"+str(nr)+"/scan", LaserScan, callback_scan)
    time.sleep(1)

def callback_pose(msg):
    global yaw_ros
    global x_ros
    global y_ros
    x_ros = msg.pose.pose.position.x
    y_ros = msg.pose.pose.position.y
    yaw_ros = get_rotation(msg.pose.pose.orientation)

def callback_scan(msg):
    i  = 0 
    for r in msg.ranges:
        if(not math.isinf(r) and not math.isnan(r)):
            temp_x = r*math.cos(theta[i])
            temp_y = r*math.sin(theta[i])
            x_g,y_g=get_global_position(temp_x,temp_y)
            updateMap(x_g,y_g)
        i = i+ 1

def get_rotation (orientation_q):
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    table_of_euler_angles = euler_from_quaternion (orientation_list)
    return table_of_euler_angles[2]

def updateMap(x,y):
    indx=int(x/resolution+trueDim/2)
    indy=int(y/resolution+trueDim/2)
    Mapa[indx][indy]=Mapa[indx][indy]+inverse_sensor_model
    Update(int(x_ros/resolution+trueDim/2),int(y_ros/resolution+trueDim/2),indx,indy)

def get_global_position(x,y):
    x=x+0.18
    x_g = x_ros + math.cos(yaw_ros)*x - math.sin(yaw_ros)*y
    y_g = y_ros + math.sin(yaw_ros)*x  + math.cos(yaw_ros)*y
    return x_g,y_g

def plotLineLow(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy
    D = (2 * dy) - dx
    y = y0

    for x in range(x0,x1):
        Mapa[x][y]=Mapa[x][y]+freePointConstant
        if D > 0:
            y = y + yi
            D = D + (2 * (dy - dx))
        else:
            D = D + 2*dy
def plotLineHigh(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    D = (2 * dx) - dy
    x = x0

    for y in range(y0,y1):
        Mapa[x][y]=Mapa[x][y]+freePointConstant
        if D > 0:
            x = x + xi
            D = D + (2 * (dx - dy))
        else:
            D = D + 2*dx
def Update(x0,y0,x1,y1):
    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            plotLineLow(x1, y1, x0, y0)
        else:
            plotLineLow(x0, y0, x1, y1)
    else:
        if y0 > y1:
            plotLineHigh(x1, y1, x0, y0)
        else:
            plotLineHigh(x0, y0, x1, y1)
def wavefront(xstart,ystart,xfinish,yfinish,Map):
    startIdx=int(xstart/resolution+trueDim/2)
    startIdy=int(ystart/resolution+trueDim/2)
    finishIdx=int(xfinish/resolution+trueDim/2)
    finishIdy=int(yfinish/resolution+trueDim/2)
    WavefrontMap=np.copy(Map)
    WavefrontMap[WavefrontMap>0.5]=np.Inf
    WavefrontMap[WavefrontMap<=0.5]=-2
    WavefrontMap[finishIdx][finishIdy]=0
    tempMap=np.copy(WavefrontMap)
    while WavefrontMap[startIdx][startIdy]==-2:
        for i in range(trueDim):
            for j in range(trueDim):
                if WavefrontMap[i][j]==-2:
                    if i+1<trueDim and WavefrontMap[i+1][j]!= -2 and WavefrontMap[i+1][j]!= np.Inf:
                        tempMap[i][j]=WavefrontMap[i+1][j]+1
                    if i-1>0 and WavefrontMap[i-1][j]!= -2 and WavefrontMap[i-1][j]!= np.Inf:
                        tempMap[i][j]=WavefrontMap[i-1][j]+1
                    if j+1<trueDim and WavefrontMap[i][j+1]!= -2 and WavefrontMap[i][j+1]!= np.Inf:
                        tempMap[i][j]=WavefrontMap[i][j+1]+1
                    if j-1>0 and WavefrontMap[i][j-1]!= -2 and WavefrontMap[i][j-1]!= np.Inf:
                        tempMap[i][j]=WavefrontMap[i][j-1]+1
        WavefrontMap=np.copy(tempMap)
    path=[]
    z=WavefrontMap[startIdx][startIdy]
    indx=startIdx
    indy=startIdy
    path.append((indx,indy))
    while z !=0:
        if indx+1<trueDim and WavefrontMap[indx+1][indy]<z:
            z=WavefrontMap[indx+1][indy]
            indx=indx+1
            path.append((indx,indy))
            continue
        if indx-1>0 and WavefrontMap[indx-1][indy]<z:
            z=WavefrontMap[indx-1][indy]
            indx=indx-1
            path.append((indx,indy))
            continue
        if indy+1<trueDim and WavefrontMap[indx][indy+1]<z:
            z=WavefrontMap[indx][indy+1]
            indy=indy+1
            path.append((indx,indy))
            continue
        if indy-1>0 and WavefrontMap[indx][indy-1]<z:
            z=WavefrontMap[indx][indy-1]
            indy=indy-1
            path.append((indx,indy))
            continue
    return path
    

def log2percent(num):
    return 1-1/(1+math.exp(num))
def getProbability():
    shape=Mapa.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            MapaProb[i][j]= 1-1/(1+np.exp(Mapa[i][j]))
#print(len(data))
#for i in range(len(data)):
    #x_ros=data[i]["pose"][0]
    #y_ros=data[i]["pose"][1]
    #yaw_ros=math.radians(data[i]["pose"][2])
    #callback_scan(data[i]["scan"])


finishx=4
finishy=-3
viridis = cm.get_cmap('Blues', 256)
newcolors = viridis(np.linspace(0, 1, 256))
pink = np.array([248/256, 24/256, 148/256, 1])
newcolors[255, :] = pink
newcmp = ListedColormap(newcolors)
listener()
getProbability()
path=wavefront(x_ros,y_ros,finishx,finishy,Mapa)
for point in path:
        MapaProb[point[0]][point[1]]=1.01
ax=plt.imshow(MapaProb,interpolation="nearest",cmap=newcmp)
plt.colorbar()
plt.ion()
while 1:
    #plt.imshow(Mapa, interpolation="nearest")
    getProbability()
    path=wavefront(x_ros,y_ros,finishx,finishy,Mapa)
    for point in path:
        MapaProb[point[0]][point[1]]=35
    ax.set_data(MapaProb)
    plt.show()
    plt.pause(0.001)
