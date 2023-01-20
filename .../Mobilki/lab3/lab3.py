import numpy as np
import math
import rospy
import time
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from nav_msgs.msg import OccupancyGrid
import matplotlib as mpl
import matplotlib.pyplot as plt
from tf.transformations import euler_from_quaternion, quaternion_from_euler

mapDim=[20,20]
resolution=0.05
pHit=0.95
pMiss=0.05
pFree=0.40
inverse_sensor_model=math.log(pHit/(1-pHit))
freePointConstant=math.log(pFree/(1-pFree))
Mapa=np.zeros([int(mapDim[0]/resolution),int(mapDim[1]/resolution)],dtype=float)
MapaProb=np.zeros([int(mapDim[0]/resolution),int(mapDim[1]/resolution)],dtype=float)
Occuppancy=OccupancyGrid()
Occuppancy.header.frame_id=str(1)
Occuppancy.info.resolution=resolution
Occuppancy.info.width=int(mapDim[0]/resolution)
Occuppancy.info.height=int(mapDim[1]/resolution)
Occuppancy.info.origin.position.x=20
Occuppancy.info.origin.position.y=20
trueDim=len(Mapa)
nr=2
x = np.arange(0,512)
theta = (np.pi/512 )*(x-256) 
x_ros=0
y_ros=0
yaw_ros=0
map_pub=0
def listener():
    global map_pub
    rospy.init_node('grupa5_scan_subscriber', anonymous=True)
    rospy.Subscriber('/PIONIER'+str(nr)+'/RosAria/pose', Odometry, callback_pose)
    time.sleep(1)
    rospy.Subscriber("/PIONIER"+str(nr)+"/scan", LaserScan, callback_scan)
    time.sleep(1)
    map_pub = rospy.Publisher('map', OccupancyGrid, queue_size=2)

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

def get_rotation (orientation_q):
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    table_of_euler_angles = euler_from_quaternion (orientation_list)
    return table_of_euler_angles[2]

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
def getProbability():
    shape=Mapa.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            MapaProb[i][j]= 1-1/(1+np.exp(Mapa[i][j]))
def publishMap():
    map8int=(MapaProb*100).astype(dtype=np.int8)
    Occuppancy.header.stamp=rospy.Time()
    Occuppancy.data=map8int.flatten()
    map_pub.publish(Occuppancy)
		
listener()
getProbability()
ax=plt.imshow(MapaProb, interpolation="nearest",cmap='Blues')
plt.colorbar()
plt.ion()
while 1:
    #plt.imshow(Mapa, interpolation="nearest",cmap='Blues')
    getProbability()
    publishMap()
    ax.set_data(MapaProb)
    plt.show()
    plt.pause(0.001)
