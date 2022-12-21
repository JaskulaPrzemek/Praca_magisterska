#!/usr/bin/env python
import numpy as np
import math
import rospy
import time
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
from gazebo_msgs.srv import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from tf.transformations import euler_from_quaternion, quaternion_from_euler

Class GazeboCommunication:
	def __init__(self):
	rospy.init_node('PythonNode', anonymous=True)
	rospy.Subscriber('/pioneer2dx/odom', Odometry, self.callback_odom)
	rospy.Subscriber('/sonar', Range, self.callback_range)
	self.cmd_publisher=rospy.Publisher('/pioneer2dx/cmd_vel', Twist, queue_size=2)
	self.cmd=Twist()
	self.modelList=[]
	
	def callback_odom(msg):
	self.robot_x=msg.pose.pose.position.x
   	self.robot_y=msg.pose.pose.position.y
   	orientation_q=msg.pose.pose.orientation
   	orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    	table_of_euler_angles = euler_from_quaternion (orientation_list)
   	self.robot_angle=table_of_euler_angles[2]
   	
   	def callback_range(msg):
   	self.robot_range=msg._Range
   	
   	def spawnPioneer(self,x,y):
   	initial_pose = Pose()
    	initial_pose.position.x = x
    	initial_pose.position.y = y
    	initial_pose.position.z = 0
    	model_path = '/home/pszemek/Desktop/Projekt_Specjalnosciowy/catkin_ws/src/pioneer2dx_test/model.sdf'

	with open (model_path, 'r') as xml_file:
		model_xml = xml_file.read().replace('\n', '')
	rospy.wait_for_service('gazebo/spawn_sdf_model')
	spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
	spawn_model_prox('Pioneer2DX', model_xml, '', initial_pose, 'world')
	
   	def updateModelList(self):
   	
   	
   	def deleteModel(self,modelName):
   	rospy.wait_for_service("gazebo/delete_model")
   	delete_model = rospy.ServicePoxy("gazebo/delete_model", DeleteModel)
   	delete_model(modelName)
   	
   	def spawnWall(self,x1,y1,x2,y2):
   	midx=(x1+x2)/2
	midy=(y1+y2)/2
	lenght=math.sqrt((x1-x2)**2 +(y1-y2)**2)
	if (x2-x1)==0:
		angle=math.pi/2;
	else:
		angle=math.atan((y2-y1)/(x2-x1));
		
   	model_path = '/home/pszemek/Desktop/Projekt_Specjalnosciowy/catkin_ws/src/Wall/model.sdf'

	with open (model_path, 'r') as xml_file:
		model_xml = xml_file.read().replace('\n', '')
	rospy.wait_for_service('gazebo/spawn_sdf_model')
	spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
	spawn_model_prox('Pioneer2DX', model_xml, '', initial_pose, 'world')
	
