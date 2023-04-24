import os
import matplotlib as plt
import numpy as np
import Mapa as mp
import FPA as f
import APF as a
import WOA as w
import random

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


def avg(lst):
    return sum(lst) / len(lst)


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
    begList = []
    flag = False
    with open("wyniki/" + mapstr + "/" + stratStr + ".txt") as file:
        for line in file:
            beggining = line[:2]
            beggining = beggining.strip()
            end = line[-2:]
            if beggining != "[" and flag or end == " \n" and flag:
                flag = False
                Qstring += line
                Qstring = Qstring.strip()
                Qstring = Qstring.replace("]\n", "];")
                Array = np.matrix(Qstring, dtype=float)
                Qlist.append(Array)
            if flag:
                Qstring += line
            if beggining == "Q" or beggining == "\n":
                Qstring = ""
                Qstring += line[2:]
                flag = True
    return Qlist


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


def getDataForAMap(mapstr):
    m = reconstructMap(mapstr)
    if not os.path.exists("plots/" + mapstr):
        os.makedirs("plots/" + mapstr, exist_ok=True)
    fig = m.viewMap(False)
    fig.savefig("plots/" + mapstr + "/mapa.png", bbox_inches="tight")
    PossibleMaps = ["Zero", "APF", "FPA", "WOA", "NN"]
    for map in PossibleMaps:
        Qlist = reconstructQList(mapstr, map)
        (
            TimeList,
            QTimeList,
            StepList,
            PathList,
            LenghtList,
            SmoothnesList,
        ) = getAllLists(mapstr, map)
        for index, value in enumerate(StepList):
            StepList[index] = avg(value)
        with open("plots/" + mapstr + "/statData.txt", "a") as file:
            file.write(map + "\n")
            file.write(
                f"Time Min {'%.3f' % min(TimeList)} Max {'%.3f' % max(TimeList)} Avg {'%.3f' % avg(TimeList)} \n"
            )
            file.write(
                f"QTime Min {'%.3f' % min(QTimeList)} Max {'%.3f' % max(QTimeList)} Avg {'%.3f' % avg(QTimeList)} \n"
            )
            file.write(
                f"Lenght Min {'%.3f' % min(LenghtList)} Max {'%.3f' % max(LenghtList)} Avg {'%.3f' % avg(LenghtList)} \n"
            )
            file.write(
                f"Smoothnes Min {'%.3f' % min(SmoothnesList)} Max {'%.3f' % max(SmoothnesList)} Avg {'%.3f' % avg(SmoothnesList)} \n"
            )
            file.write(
                f"Step Min {'%.3f' % min(StepList)} Max {'%.3f' % max(StepList)} Avg {'%.3f' % avg(StepList)} \n"
            )
        for index, path in enumerate(PathList):
            if type(path) == float:
                continue
            fig = m.plotFromPath(path, False)
            fig.savefig("plots/" + mapstr + "/" + map + str(index) + ".png")


def generateLatexTableTime_Qtime(mapstr):
    LatexStr = """
\\begin{table}[]
\centering
\\begin{tabular}{l|llllll}
\cline{2-7}
& \multicolumn{1}{l|}{$Time_{Min}$} & \multicolumn{1}{l|}{$Time_{Max}$} & \multicolumn{1}{l|}{$Time_{Avg}$} & \multicolumn{1}{l|}{$QTime_{Min}$} & \multicolumn{1}{l|}{$QTime_{Max}$} & \multicolumn{1}{l|}{$QTime_{Avg}$} \\\\ \hline
    """
    Numbers = []
    PossibleMaps = ["Zero", "APF", "FPA", "WOA", "NN"]

    with open("plots/" + mapstr + "/statData.txt") as file:
        for line in file:
            lista = line.split(" ")
            if "Time" in lista:
                Numbers.append(lista[2])
                Numbers.append(lista[4])
                Numbers.append(lista[6])
            if "QTime" in lista:
                Numbers.append(lista[2])
                Numbers.append(lista[4])
                Numbers.append(lista[6])
    map_index = -1
    for index, value in enumerate(Numbers):
        if index % 6 == 0:
            if map_index != -1:
                str = str[:-1]
                str += "\\\\ \cline{1-1} \n"
                LatexStr += str
            map_index += 1
            # print(map_index)
            str = "\multicolumn{1}{|l|}{" + f" {PossibleMaps[map_index]}" + "} &"
        str += value + "&"
    LatexStr += str[:-1] + "\\\\ \cline{1-1} \n"
    # LatexStr = LatexStr[:-1]
    LatexStr += """
    \end{tabular}
    \end{table}
    """

    print(LatexStr)


def generateLatexTableRest(mapstr):
    LatexStr = """
\\begin{table}[]
\centering
\\resizebox{\\textwidth}{!}{%
\\begin{tabular}{l|llllllll}
\cline{2-9}
 &
  \multicolumn{1}{l|}{$Lenght_{Min}$} &
  \multicolumn{1}{l|}{$Lenght_{Max}$} &
  \multicolumn{1}{l|}{$Lenght_{Avg}$} &
  \multicolumn{1}{l|}{$Smoothness_{Min}$} &
  \multicolumn{1}{l|}{$Smoothness_{Max}$} &
  \multicolumn{1}{l|}{$Smoothness_{Avg}$} &
  \multicolumn{1}{l|}{$Step_{Max}$} &
  \multicolumn{1}{l|}{$Step_{Avg}$} \\\\ \hline
          """
    Numbers = []
    PossibleMaps = ["Zero", "APF", "FPA", "WOA", "NN"]

    with open("plots/" + mapstr + "/statData.txt") as file:
        for line in file:
            lista = line.split(" ")
            if "Lenght" in lista:
                Numbers.append(lista[2])
                Numbers.append(lista[4])
                Numbers.append(lista[6])
            if "Smoothnes" in lista:
                Numbers.append(lista[2])
                Numbers.append(lista[4])
                Numbers.append(lista[6])
            if "Step" in lista:
                Numbers.append(lista[4])
                Numbers.append(lista[6])
    map_index = -1
    for index, value in enumerate(Numbers):
        if index % 8 == 0:
            if map_index != -1:
                str = str[:-1]
                str += "\\\\ \cline{1-1} \n"
                LatexStr += str
            map_index += 1
            # print(map_index)
            str = "\multicolumn{1}{|l|}{" + f" {PossibleMaps[map_index]}" + "} &"
        str += value + "&"
    LatexStr += str[:-1] + "\\\\ \cline{1-1} \n"
    # LatexStr = LatexStr[:-1]
    LatexStr += """
    \end{tabular}%
    }
    \end{table}
    """

    print(LatexStr)


def genLatexPaths(mapstr):
    PossibleMaps = ["Zero", "APF", "FPA", "WOA", "NN"]
    for map in PossibleMaps:
        i = random.randint(0, 9)
        if map == "FPA":
            i = i * 2
        latexStr = (
            """
        \\begin{frame}
        \centering
        """
            + map
            + """
        \includegraphics[width=\\textwidth,height=\\textheight]{Obrazy/"""
            + mapstr
        )
        latexStr += (
            """/"""
            + map
            + str(i)
            + """.png}
    \end{frame}
        """
        )
        print(latexStr)


def genLatexBeamer(map):
    str = (
        """
        \\begin{frame}
    \centering
    \includegraphics[width=\\textwidth,height=\\textheight]{Obrazy/"""
        + map
        + """/mapa.png}
    \end{frame}
    \\begin{frame}
    \centering
        """
    )
    print(str)
    generateLatexTableTime_Qtime(map)
    print(
        """
        \end{frame}
    \\begin{frame}
    \centering
        """
    )
    generateLatexTableRest(map)
    print(
        """
        \end{frame}
        """
    )


AllList = [
    "map1",
    "map2",
    "map3",
    "map4",
    "map5",
    "randMap/rand1",
    "randMap/rand2",
    "randMap/rand3",
    "randMap/rand4",
    "randMap/rand5",
]
for mapstr in AllList:
    genLatexBeamer(mapstr)
    genLatexPaths(mapstr)
# getDataForAMap("map1")
# getDataForAMap("map2")
# getDataForAMap("map3")
# getDataForAMap("map4")
# getDataForAMap("map5")
# getDataForAMap("randMap/rand1")
# getDataForAMap("randMap/rand2")
# getDataForAMap("randMap/rand3")
# getDataForAMap("randMap/rand4")
# getDataForAMap("randMap/rand5")
