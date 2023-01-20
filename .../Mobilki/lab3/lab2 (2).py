
#!/usr/bin/env python

# run: python subscriber_scan.py 5  (where 5 is robot number)
import json
import sys
import rospy
from sensor_msgs.msg import LaserScan
import tf
import math 
import time
from nav_msgs.msg import Odometry
import datetime
from tf.transformations import euler_from_quaternion, quaternion_from_euler



class Point:
    X = 0
    Y = 0
    def __init__(self, x, y):
        self.X = x
        self.Y = y

resolution = 0.006135923322290182
angle_start = -1.5707963705062866
data_sacn = []
data_row = []

x_ros = 0 
y_ros = 0
yaw_ros = 0
start_time = 0



def callback_scan(msg):
    global data_sacn
    global data_row

    i  = 0 
    data_sacn.clear()
    data_row = msg
    for r in msg.ranges:
        if(not math.isinf(r)):
          theta =   angle_start + i* resolution 
          temp_x = r*math.cos(theta)
          temp_y = r*math.sin(theta)
          data_sacn.append(Point(temp_x,temp_y))
        
        i = i+ 1
        


def callback_pose(msg):
   global x_ros
   global y_ros
   global yaw_ros 
   x_ros = msg.pose.pose.position.x
   y_ros = msg.pose.pose.position.y
   yaw_ros = get_rotation(msg.pose.pose.orientation)


def get_rotation (orientation_q):
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    table_of_euler_angles = euler_from_quaternion (orientation_list)
    return table_of_euler_angles

    

def listener():

    rospy.init_node('grupa5_scan_subscriber', anonymous=True)
    rospy.Subscriber("/PIONIER"+nr+"/scan", LaserScan, callback_scan)
    rospy.Subscriber('/PIONIER'+nr+'/RosAria/wheels', Odometry, callback_pose)
    
    # rospy.spin()


def write_to_row_json(list):
    title = "Pionier_"+str(nr)+"_raw.json"
    with open(title, "w") as outfile:
        json.dump(list , outfile)


def create_dict_to_json():
    global data_row
    global x_ros
    global y_ros
    global yaw_ros
    global start_time

    temp_pose = [x_ros, yaw_ros, yaw_ros]
    time_now = time.time() - start_time
    dict = {
        "pose": temp_pose,
        "time": time_now, 
        "scan": data_row.ranges
    }
    return dict


def prepere_list_of_mesurment(time_action):
    list_of_mesurments = []
    start = time.time()
    while(True):
        if (time.time() - start) >= time_action:
            break
        temp_dic = create_dict_to_json()
        list_of_mesurments.append(temp_dic)
        time.sleep(0.05)
    

    return list_of_mesurments



def write_XY_to_json():
    global data_sacn
    data = []
    
    for p in data_sacn:
        temp_dict = {
        "X": p.X,
        "Y": p.Y
        }
        data.append(temp_dict)
        
    with open("Pionier_1.json", "w") as outfile:
        json.dump(data , outfile)



if __name__ == '__main__':
    start_time
    start_time = time.time()

    if len(sys.argv) < 2:
        sys.stderr.write('Usage: sys.argv[0] \n')
        sys.exit(1)
    nr=sys.argv[1]
    listener()

  
    time.sleep(2)
    write_to_row_json(prepere_list_of_mesurment(1))
  


