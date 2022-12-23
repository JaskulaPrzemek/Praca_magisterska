import math
import rospy

import gazeboCommunication as gzlib
import Mapa as mp
#spawnWall(1,2,2,1)
gz=gzlib.GazeboCommunication()
gz.updateModelList()
print(gz.modelList)
gz.spawnPioneer(2,2)
print(gz.updateModelList())
Mapa=mp.Map()
Mapa.createMap(1)
Mapa.createCMap()
Mapa.createGazeboMap()

