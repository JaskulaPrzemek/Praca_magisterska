#!/usr/bin/env python
import numpy as np
import math
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
from geometry_msgs.msg import Pose
from gazebo_msgs.srv import *
import xml.dom.minidom as md
from tf.transformations import euler_from_quaternion

class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
class GazeboCommunication(metaclass=SingletonMeta):
	def __init__(self):
		rospy.init_node('PythonNode', anonymous=True)
		rospy.Subscriber('/pioneer2dx/odom', Odometry, self.callback_odom)
		rospy.Subscriber('/sonar', Range, self.callback_range)
		self.cmd_publisher=rospy.Publisher('/pioneer2dx/cmd_vel', Twist, queue_size=2)
		self.cmd=Twist()
		self.modelList=[]
	
	def callback_odom(self,msg):
		self.robot_x=msg.pose.pose.position.x
		self.robot_y=msg.pose.pose.position.y
		orientation_q=msg.pose.pose.orientation
		orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
		table_of_euler_angles = euler_from_quaternion (orientation_list)
		self.robot_angle=table_of_euler_angles[2]
   	
	def callback_range(self,msg):
		print(msg)
		self.robot_range=msg.range
   	
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
		rospy.wait_for_service('gazebo/get_world_properties')
		world_prop_proxy=rospy.ServiceProxy('gazebo/get_world_properties', GetWorldProperties)
		result=world_prop_proxy()
		self.modelList=result.model_names
		return result.model_names
   		
   	
	def deleteModel(self,modelName):
		rospy.wait_for_service("gazebo/delete_model")
		delete_model = rospy.ServiceProxy("gazebo/delete_model", DeleteModel)
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
		model=md.parse(model_path)
		sizeval =f'{lenght:.6f}' " 0.01 2.5"
		pose1val = f'{midx:.6f}'+" "+f'{midy:.6f}' + " 0 0 -0 0"
		pose2val = pose2val="-0 0 0 0 -0 "+f'{angle:.6f}'
		posy=model.getElementsByTagName("pose")
		posy[0].childNodes[0].nodeValue=pose1val
		posy[3].childNodes[0].nodeValue=pose2val
		sizy=model.getElementsByTagName("size")
		sizy[0].childNodes[0].nodeValue=sizeval
		sizy[1].childNodes[0].nodeValue=sizeval
		name=model.getElementsByTagName("model")[0].getAttribute('name')
		self.updateModelList()
		objnum=0
		tname=name
		while(1):
			print(tname)
			indx=self.modelList.count(tname)
			if indx !=0:
				tname=name+"_"+str(objnum)
				objnum=objnum+1
			else:
				break
		
		rospy.wait_for_service('gazebo/spawn_sdf_model')
		initial_pose=Pose()
		initial_pose.position.x=0
		initial_pose.position.y=0
		initial_pose.position.z=0
		initial_pose.orientation.w = 1
		initial_pose.orientation.x = 0
		initial_pose.orientation.y = 0
		initial_pose.orientation.z = 0
		spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
		spawn_model_prox(tname, model.toxml(), '', initial_pose, 'world')

