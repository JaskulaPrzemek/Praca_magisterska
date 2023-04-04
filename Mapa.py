#!/usr/bin/env python
import numpy as np
from matplotlib.path import Path
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import gazeboCommunication as gzlib
import random


class Map:
    def __init__(self):
        self.size = (20, 20)
        self.obstacles = []

    def createMap(self, type=1):
        self.size = (20, 20)
        self.obstacles = []
        if type == -1:
            self.startingPoint = (2, 16)
            self.target = (19, 16)
        if type == 0:
            self.startingPoint = (2, 16)
            self.target = (19, 16)
            self.obstacles.append([(10, 16, 2)])
        if type == 1:
            self.startingPoint = (2, 16)
            self.target = (19, 11)
            self.obstacles.append([(2, 9), (2, 12), (4, 12), (2, 9)])
            self.obstacles.append([(4, 6, 1)])
            self.obstacles.append([(3, 3), (4, 2), (6, 2), (7, 3), (3, 3)])
            self.obstacles.append([(3, 14), (2, 18), (5, 18), (3, 14)])
            self.obstacles.append([(6, 12), (8, 13), (10, 12), (9, 14), (
                10, 15), (9, 16), (8, 18), (7, 16), (6, 15), (7, 14), (6, 12)])
            self.obstacles.append(
                [(9, 4), (11, 4), (11, 8), (12, 8), (12, 10), (10, 10), (10, 6), (9, 6), (9, 4)])
            self.obstacles.append([(18, 14), (16, 18), (20, 14), (18, 14)])
            self.obstacles.append([(16, 10), (15, 12), (18, 12), (16, 10)])
            self.obstacles.append([(13, 3), (14, 3), (15, 2), (16, 3), (17, 2),
                                  (18, 4), (17, 5), (15, 4), (14, 5), (13, 5), (13, 3)])
        if type == 2:
            self.startingPoint = (2, 16)
            self.target = (19, 11)
            for i in range(1, 4):
                for j in range(1, 6):
                    x = 6+(i-1)*4
                    y = 6+(j-1)*3-(i-1)*2
                    self.obstacles.append(
                        [(x, y), (x, y+1), (x+1, y+1), (x+1, y), (x, y)])
        if type == 3:
            self.createRandomMap()
        if type == 4:
            self.startingPoint = (1, 11)
            self.target = (18, 11)
            self.obstacles.append(
                [(7, 15), (7, 17), (15, 17), (15, 5), (7, 5), (7, 7), (13, 7), (13, 15), (7, 15)])
        self.obstaclesShort = self.obstacles.copy()

    def createRandomMap(self):
        while True:
            nr_of_obstacles = int(random.random()*7+6)
            for i in range(nr_of_obstacles):
                p = random.random()
                flag = False
                while(not flag):
                    if p < 0.1:
                        randr = int(random.random()*2+1)
                        minx = 1+randr
                        maxx = self.size[0]-randr-minx
                        randx = int(random.random()*maxx+minx)
                        randy = int(random.random()*maxx+minx)
                        tempobstacle = [(randx, randy, randr)]
                    else:
                        if p < 0.3:
                            nr_or_vertices = 3
                        else:
                            nr_or_vertices = int(random.random()*6+4)
                        randx = int(random.random()*(self.size[0]-1)+1)
                        randy = int(random.random()*(self.size[0]-1)+1)
                        tempobstacle = [(randx, randy)]
                        z = 0
                        for j in range(nr_or_vertices-1):
                            x = -1
                            y = -1

                            while(x < 1 or x > self.size[0] or y < 1 or y > self.size[1]):
                                x = tempobstacle[j][0] + \
                                    int(random.random()*(6)-3)
                                y = tempobstacle[j][1] + \
                                    int(random.random()*(6)-3)
                                if (x, y) in tempobstacle:
                                    x = -1
                                    z += 1
                                if j > 0 and (tempobstacle[j-1][1] == y or tempobstacle[j-1][0] == x):
                                    x = -1
                                    z += 1
                                if z > 120:
                                    flag = True
                                    break
                            tempobstacle.append((x, y))
                        tempobstacle.append(tempobstacle[0])
                    if(self.checkProperObstacle(tempobstacle)):
                        self.obstacles.append(tempobstacle)
                        flag = True
            self.createCMap()
            x = int(random.random()*(self.size[0]-2)+1)
            y = int(random.random()*(self.size[0]-2)+1)
            while (self.checkInterior(x, y)):
                x = int(random.random()*(self.size[0]-2)+1)
                y = int(random.random()*(self.size[0]-2)+1)
            self.startingPoint = (x, y)
            x = int(random.random()*(self.size[0]-2)+1)
            y = int(random.random()*(self.size[0]-2)+1)
            while (self.checkInterior(x, y) or self.startingPoint == (x, y) or np.sqrt((self.startingPoint[0]-x)**2 + (self.startingPoint[1]-y)**2) < 9):
                x = int(random.random()*(self.size[0]-2)+1)
                y = int(random.random()*(self.size[0]-2)+1)
            self.target = (x, y)
            if(not wavefront(self.startingPoint, self.target, self)):
                break
            else:
                self.obstacles = []
        # for obs in self.obstacles:
        #   print(obs)

    def checkProperObstacle(self, obstacle):
        if(self.selfIntersecting(obstacle)):
            return False
        self.createCMap()
        width = self.size[0]+1
        height = self.size[1]+1
        # mode L = 8-bit pixels, black and white
        img = Image.new(mode='L', size=(width, height), color=0)
        draw = ImageDraw.Draw(img)
        if len(obstacle) == 1:
            n = 20
            xc = obstacle[0][0]
            yc = obstacle[0][1]
            r = obstacle[0][2]
            theta = np.arange(0, n)*(2*np.pi/n)
            x = xc + r*np.cos(theta)
            y = yc + r*np.sin(theta)
            obstacle = []
            for i in range(n):
                obstacle.append((x[i], y[i]))
            obstacle.append((x[0], y[0]))
        draw.polygon(obstacle, outline=1, fill=1)
        mask = np.array(img).astype('float32')
        mask[np.where(mask == 0)] = 0
        mask = mask.astype(int)
        mask = mask+self.cMap
        result = np.where(mask == 2)
        if(not np.any(result)):
            return True
        else:
            return False

    def selfIntersecting(self, obstacle):
        if len(obstacle) <= 4:
            return False
        sides = []
        for i in range(len(obstacle)-1):
            sides.append((obstacle[i], obstacle[i+1]))
        for i in range(len(sides)):
            side1 = sides[i]
            for j in range(len(sides)):
                if j == i or j == i-1 or j == i+1:
                    continue
                if(i == 0 or i == len(sides)-1):
                    if(j == 0 or j == len(sides)-1):
                        continue
                if self.lineIntersect(side1, sides[j]):
                    return True
        return False

    def lineIntersect(self, Side1, Side2):
        A = Side1[0]
        B = Side1[1]
        C = Side2[0]
        D = Side2[1]
        return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)

    def ccw(self, A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    def createCMap(self):
        width = self.size[0]+1
        height = self.size[1]+1
        # mode L = 8-bit pixels, black and white
        img = Image.new(mode='L', size=(width, height), color=0)
        draw = ImageDraw.Draw(img)
        # draw polygons
        n = 20
        theta = np.arange(0, n)*(2*np.pi/n)
        for polygon in self.obstacles:
            if len(polygon) == 1:
                xc = polygon[0][0]
                yc = polygon[0][1]
                r = polygon[0][2]
                x = xc + r*np.cos(theta)
                y = yc + r*np.sin(theta)
                polygon = [(x[i], y[i]) for i in range(0, n)]
                polygon.append((x[0], y[0]))
                # self.obstacles[index]=polygon

            draw.polygon(polygon, outline=1, fill=1)
        # replace 0 with 'value'
        mask = np.array(img).astype('float32')
        mask[np.where(mask == 0)] = 0
        self.cMap = mask.astype(int)

    def viewMap(self, show=True):
        fig, ax = plt.subplots(figsize=(6, 6))
        plt.grid()
        for polygon in self.obstacles:
            x = []
            y = []
            if len(polygon) == 1:
                n = 20
                theta = np.arange(0, n)*(2*np.pi/n)
                xc = polygon[0][0]
                yc = polygon[0][1]
                r = polygon[0][2]
                xp = xc + r*np.cos(theta)
                yp = yc + r*np.sin(theta)
                polygon = [(xp[i], yp[i]) for i in range(0, n)]
                polygon.append((xp[0], yp[0]))
                # print(polygon)
            for point in polygon:
                x.append(point[0])
                y.append(point[1])
            ax.fill(x, y)
        plt.xlim([0, self.size[0]])
        plt.ylim([0, self.size[1]])
        plt.xticks(np.arange(0, self.size[0], 2))
        plt.yticks(np.arange(0, self.size[1], 2))
        plt.plot(self.target[0], self.target[1], 'or')
        plt.plot(self.startingPoint[0], self.startingPoint[1], 'ob')
        ax.set_axisbelow(True)
        if(show):
            plt.show()
        return fig

    def plotPath(self, Q, show=True, fig=-1):
        if fig == -1:
            fig = self.viewMap(False)
        plt.figure(fig.number)
        x, y = self.getPath(Q)
        plt.plot(x, y)
        if show:
            plt.show()
        return fig

    def getPath(self, Q):
        x = []
        y = []
        state = self.startingPoint
        x.append(state[0])
        y.append(state[1])
        if np.any(Q):
            while state != self.target:
                temp = state[0]+state[1]*20 - 21
                list_Q = Q[temp].tolist()
                a = list_Q.index(max(list_Q))
                if a == 0:
                    state = (state[0]-1, state[1])
                elif a == 1:
                    state = (state[0]+1, state[1])
                elif a == 2:
                    state = (state[0], state[1]-1)
                else:
                    state = (state[0], state[1]+1)
                x.append(state[0])
                y.append(state[1])
        self.path = tuple(zip(x, y))
        self.pathLenght = len(x)
        self.pathSmoothness = self.getSmoothness(self.path)
        return x, y

    def getSmoothness(self, path):
        """
        Calculate Path smoothnes as in FPA article
        https://www.sciencedirect.com/science/article/pii/S0921889018308285
        """
        sum = 0
        for index, (x, y) in enumerate(path, start=1):
            if index >= self.pathLenght-1:
                break
            x1, y1 = path[index + 1]
            x2, y2 = path[index - 1]
            sum += abs(np.arctan2((y1-y), (x1-x)) - np.arctan2((y-y2), (x-x2)))
        return sum

    def createGazeboMap(self):
        gz = gzlib.GazeboCommunication()
        for obstacle in self.obstacles:
            for point_index in range(len(obstacle)-1):
                gz.spawnWall(obstacle[point_index][0], obstacle[point_index]
                             [1], obstacle[point_index+1][0], obstacle[point_index+1][1])

    def checkInterior(self, x, y):
        if self.cMap[y][x] == 1:
            return True
        return False

    def save(self, path="data.txt"):
        with open(path, "a") as file:
            file.write("Map: \n")
            file.write(f"S {self.startingPoint} \n")
            file.write(f"T {self.target} \n")
            file.write("O: \n")
            for obstacle in self.obstaclesShort:
                file.write(f"{str(obstacle)} \n")

    def getListRep(self):
        listRep = (np.reshape(
            self.cMap, (self.size[0]+1)*(self.size[1]+1))).tolist()
        listRep.extend(self.startingPoint)
        listRep.extend(self.target)
        return listRep

    def loadListRep(self, ListRep):
        cMap = ListRep[:-4]
        size = int(np.sqrt(len(cMap)))
        self.cMap = np.reshape(cMap, (size, size))
        self.size = (size, size)
        self.startingPoint = tuple(ListRep[-4:-2])
        self.target = tuple(ListRep[-2:])


def wavefront(start, finish, Map):
    startIdx = start[1]
    startIdy = start[0]
    finishIdx = finish[1]
    finishIdy = finish[0]
    trueDim = Map.size[0]
    WavefrontMap = np.copy(Map.cMap.astype(float))
    WavefrontMap[WavefrontMap > 0.5] = np.Inf
    WavefrontMap[WavefrontMap <= 0.5] = -2
    WavefrontMap[finishIdx][finishIdy] = 0
    tempMap = np.copy(WavefrontMap)
    while WavefrontMap[startIdx][startIdy] == -2:
        flag = True
        for i in range(trueDim):
            for j in range(trueDim):
                if(i == 0 or i == trueDim-1 or j == 0 or j == trueDim-1):
                    continue
                if WavefrontMap[i][j] == -2:
                    if i+1 < trueDim and WavefrontMap[i+1][j] != -2 and WavefrontMap[i+1][j] != np.Inf:
                        tempMap[i][j] = WavefrontMap[i+1][j]+1
                        flag = False
                    if i-1 > -1 and WavefrontMap[i-1][j] != -2 and WavefrontMap[i-1][j] != np.Inf:
                        tempMap[i][j] = WavefrontMap[i-1][j]+1
                        flag = False
                    if j+1 < trueDim and WavefrontMap[i][j+1] != -2 and WavefrontMap[i][j+1] != np.Inf:
                        tempMap[i][j] = WavefrontMap[i][j+1]+1
                        flag = False
                    if j-1 > -1 and WavefrontMap[i][j-1] != -2 and WavefrontMap[i][j-1] != np.Inf:
                        tempMap[i][j] = WavefrontMap[i][j-1]+1
                        flag = False
        WavefrontMap = np.copy(tempMap)
        if(flag):
            break
            plt.imshow(WavefrontMap)
            plt.xlim([0, trueDim])
            plt.ylim([0, trueDim])
            plt.xticks(np.arange(0, trueDim, 2))
            plt.yticks(np.arange(0, trueDim, 2))
            for obs in Map.obstacles:
                print(obs)

    return flag
