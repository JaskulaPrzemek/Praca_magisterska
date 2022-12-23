#!/usr/bin/env python
import numpy as np
from matplotlib.path import Path
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import gazeboCommunication as gzlib
class Map:
    def __init__(self):
        pass
    def createMap(self,type=1):
        self.size=(20,20)
        self.obstacles=[]
        if type == -1:
            self.startingPoint=(2,16)
            self.target=(2,16)
        if type == 0:
            self.startingPoint=(2,16)
            self.target=(2,16)
            self.obstacles.append([(10,16,2)])
        if type == 1:
            self.startingPoint=(2,16)
            self.target=(2,16)
            self.obstacles.append([(2,9),(2,12),(4,12),(2,9)])
            self.obstacles.append([(4,6,1)])
            self.obstacles.append([(3,3),(4,2),(6,2),(7,3),(3,3)])
            self.obstacles.append([(3,14),(2,18),(5,18),(3,14)])
            self.obstacles.append([(6,12),(8,13),(10,12),(9,14),(10,15),(9,16),(8,18),(7,16),(6,15),(7,14),(6,12)])
            self.obstacles.append([(9,4),(11,4),(11,8),(12,8),(12,10),(10,10),(10,6),(9,6),(9,4)])
            self.obstacles.append([(18,14),(16,18),(20,14),(18,14)])
            self.obstacles.append([(16,10),(15,12),(18,12),(16,10)])
            self.obstacles.append([(13,3),(14,3),(15,2),(16,3),(17,2),(18,4),(17,5),(15,4),(14,5),(13,5),(13,3)])
        if type == 2:
            self.startingPoint=(2,16)
            self.target=(2,16)
            for i in  range(1,4):
                for j in range(1,6):
                    x=6+(i-1)*4
                    y=6+(j-1)*3-(i-1)*2
                    self.obstacles.append([(x,y),(x,y+1),(x+1,y+1),(x+1,y),(x,y)])
    def createRandomMap(self):
        pass
    def createCMap(self):
        width =self.size[0]+1
        height=self.size[1]+1
        img = Image.new(mode='L', size=(width, height), color=0)  # mode L = 8-bit pixels, black and white
        draw = ImageDraw.Draw(img)
        # draw polygons
        for polygon in self.obstacles:
            if len(polygon)==1:
                index=self.obstacles.index(polygon)
                n=20
                xc=polygon[0][0]
                yc=polygon[0][1]
                r=polygon[0][2]
                theta= np.arange(0,n)*(2*np.pi/n)
                x=xc+ r*np.cos(theta)
                y=yc + r*np.sin(theta)
                polygon=[]
                for i in range(n):
                    polygon.append((x[i],y[i]))
                polygon.append((x[0],y[0]))
                self.obstacles[index]=polygon
                
            draw.polygon(polygon, outline=1, fill=1)
        # replace 0 with 'value'
        mask = np.array(img).astype('float32')
        mask[np.where(mask == 0)] = 0
        self.cMap=mask.astype(np.int)

    def viewMap(self,show=True):
        fig, ax = plt.subplots(figsize=(6, 6))
        plt.grid()
        for polygon in self.obstacles:
            x=[]
            y=[]
            for point in polygon:
                x.append(point[0])
                y.append(point[1])
            ax.fill(x,y)
        plt.xlim([0,self.size[0]])
        plt.ylim([0,self.size[1]])
        plt.xticks(np.arange(0,self.size[0],2))
        plt.yticks(np.arange(0,self.size[1],2))
        ax.set_axisbelow(True)
        if(show):
            plt.show()
        return fig
    def createGazeboMap(self):
        gz=gzlib.GazeboCommunication()
        for obstacle in self.obstacles:
            for point_index in range (len(obstacle)-1):
                gz.spawnWall(obstacle[point_index][0],obstacle[point_index][1],obstacle[point_index+1][0],obstacle[point_index+1][1])
    def checkInterior(self,x,y):
        if self.cMap[y][x]==1:
            return True
        return False
        