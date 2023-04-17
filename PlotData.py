import matplotlib as plt
import numpy as np
import Mapa as mp
import FPA as f
import APF as a
import WOA as w

# import NN as n
NNBool = False
WOABool = False
APFBool = True
FPABool = False


def getAllLists(mapstr, stratStr):
    """
    param:
    mapstr,stratStr
    usage:
    with open("wyniki/" + mapstr + "/" + stratStr + ".txt") as file:
    return TimeList, QTimeList, StepList, PathList, LenghtList, SmoothnesList"""
    TimeList = []
    QTimeList = []
    StepList = []
    PathList = []
    LenghtList = []
    SmoothnesList = []
    with open("wyniki/" + mapstr + "/" + stratStr + ".txt") as file:
        for line in file:
            beggining = line[:2]
            beggining = beggining.rstrip()
            if beggining == "t":
                TimeList.append(float(line[2:]))
            if beggining == "Qt":
                QTimeList.append(float(line[2:]))
            if beggining == "st":
                StepList.append(eval(line[3:]))
            if beggining == "p":
                PathList.append(eval(line[2:]))
            if beggining == "l":
                LenghtList.append(float(line[2:]))
            if beggining == "s":
                SmoothnesList.append(float(line[2:]))
    return TimeList, QTimeList, StepList, PathList, LenghtList, SmoothnesList


def reconstructMap(mapstr):
    """
    param:
    mapstr
    usage:
    with open("wyniki/" + mapstr + "/ZeroMap.txt") as file:

    return mapa
    """
    mapa = mp.Map()
    obstacles = []
    with open("wyniki/" + mapstr + "/ZeroMap.txt") as file:
        for line in file:
            beggining = line[:2]
            beggining = beggining.rstrip()
            if beggining == "S":
                Start = eval(line[2:])
            elif beggining == "T":
                Target = eval(line[2:])
            elif beggining == "W":
                Size = eval(line[2:])
            elif beggining == "O:" or beggining == "Ma":
                pass
            else:
                obstacles.append(eval(line))
    mapa.obstacles = obstacles
    mapa.target = Target
    mapa.startingPoint = Start
    mapa.size = Size
    mapa.createCMap()
    return mapa


def reconstructQiList(mapstr, stratStr):
    Qlist = []
    flag = False
    with open("wyniki/" + mapstr + "/" + stratStr + ".txt") as file:
        for line in file:
            beggining = line[:2]
            beggining = beggining.rstrip()
            if beggining == "Ql" and flag:
                flag = False
                Qstring = Qstring.strip()
                Qstring = Qstring.replace("]\n", "];")
                Array = np.matrix(Qstring, dtype=float)
                print(Array)
                Qlist.append(Array)
            if flag:
                Qstring += line
            if beggining == "Qi":
                Qstring = ""
                Qstring += line[2:]
                flag = True


def reconstructQList(mapstr, stratStr):
    Qlist = []
    flag = False
    with open("wyniki/" + mapstr + "/" + stratStr + ".txt") as file:
        for line in file:
            beggining = line[:2]
            beggining = beggining.strip()
            if beggining != "[" and flag:
                flag = False
                Qstring = Qstring.strip()
                Qstring = Qstring.replace("]\n", "];")
                Array = np.matrix(Qstring, dtype=float)
                print(Array)
                Qlist.append(Array)
            if flag:
                Qstring += line
            if beggining == "Q":
                Qstring = ""
                Qstring += line[2:]
                flag = True


def reconstructWOA(mapstr):
    woa = w.WOA()
    with open("wyniki/" + mapstr + "/WOA.txt") as file:
        for line in file:
            beggining = line[:2]
            beggining = beggining.rstrip()
        if beggining == "i":
            woa.iterations = int(line[2:])
        if beggining == "b":
            woa.b = float(line[2:])
        if beggining == "iA":
            woa.initA = float(line[2:])
        if beggining == "pb":
            woa.probability = float(line[2:])
        if beggining == "ps":
            woa.populationSize = int(line[2:])
    return woa


def reconstructAPF(mapstr):
    apf = a.APF()
    with open("wyniki/" + mapstr + "/APF.txt") as file:
        for line in file:
            beggining = line[:2]
            beggining = beggining.rstrip()
            if beggining == "as":
                apf.atractScale = float(line[2:])
            elif beggining == "D":
                apf.distance = float(line[2:])


def reconstructFPA(mapstr):
    fpa = f.FPA()
    with open("wyniki/" + mapstr + "/FPA.txt") as file:
        for line in file:
            beggining = line[:2]
            beggining = beggining.rstrip()
            if beggining == "ga":
                fpa.gamma = float(line[2:])
            if beggining == "i":
                fpa.iterations = int(line[2:])
            if beggining == "ug":
                fpa.updateGamma = float(line[2:])
            if beggining == "ua":
                fpa.updateAlpha = float(line[2:])
            if beggining == "ps":
                fpa.populationSize = int(line[2:])
            if beggining == "p":
                fpa.probability = float(line[2:])
            if beggining == "b":
                fpa.beta = float(line[2:])


m = reconstructMap("randMap/rand2")
qlist = reconstructQList("map2", "FPA")
print()
m.viewMap()
TimeList, QTimeList, StepList, PathList, LenghtList, SmoothnesList = getAllLists(
    "map1", "Zero"
)
getAllLists("randMap/rand1", "Zero")
