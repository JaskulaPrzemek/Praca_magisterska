try:
    import rospy
    import gazeboCommunication as gzlib
except ImportError:
    pass
import os
import Mapa as mp
import Qlearning as Q
import FPA as f
import APF as a
import WOA as w
import NN as n
from Wrapper import weirdWrapper
from RandomInitialization import randomInit
from PlotData import reconstructMap

NNBool = True
WOABool = False
APFBool = False
FPABool = False
WrapFPABool = False
WrapWOABool = False
RandBool = True
ZeroBool = False
iterations = 10
Qlearning = Q.Qlearning()
Qlearning.setEpsilon(0.05)
if FPABool:
    FPA = f.FPA()
if WOABool:
    WOA = w.WOA()
if APFBool:
    APF = a.APF()
if NNBool:
    NN = n.NN()
    NN.load("Models/NewTest/MseAdamNorm.keras")
    NN1 = n.NN()
    NN1.load("Models/NewTest/MseAdamWrapW.keras")
    NN2 = n.NN()
    NN2.load("Models/NewTest/MseAdamWrapF.keras")
if WrapFPABool:
    WrapFPA = weirdWrapper(flag=True)
if WrapWOABool:
    WrapWOA = weirdWrapper(flag=False)
if RandBool:
    RandInit = randomInit()
    RandInit.scale = 0.05


def genForMap(Qlearning, mapstr):
    global iterations
    global APFBool
    global FPABool
    global WOABool
    global NNBool
    if not os.path.exists("wyniki/" + mapstr):
        os.makedirs("wyniki/" + mapstr, exist_ok=True)
    for i in range(iterations):
        Qlearning.resetStrategy()
        if ZeroBool:
            Qlearning.learn()
            if not i:
                MapBool = True
            else:
                MapBool = False
            Qlearning.save("wyniki/" + mapstr + "/Zero.txt", mapa=MapBool)
        if FPABool:
            Qlearning.setStrategy(FPA)
            Qlearning.learn()
            Qlearning.save("wyniki/" + mapstr + "/FPA.txt", mapa=False)
        if APFBool:
            Qlearning.setStrategy(APF)
            Qlearning.learn()
            Qlearning.save("wyniki/" + mapstr + "/APF.txt", mapa=False)
        if WOABool:
            Qlearning.setStrategy(WOA)
            Qlearning.learn()
            Qlearning.save("wyniki/" + mapstr + "/WOA.txt", mapa=False)
        if NNBool:
            Qlearning.setStrategy(NN)
            Qlearning.learn()
            Qlearning.save("wyniki/" + mapstr + "/NNnorm.txt", mapa=False)
            Qlearning.setStrategy(NN1)
            Qlearning.learn()
            Qlearning.save("wyniki/" + mapstr + "/NNWrapW.txt", mapa=False)
            Qlearning.setStrategy(NN2)
            Qlearning.learn()
            Qlearning.save("wyniki/" + mapstr + "/NNWrapF.txt", mapa=False)
        if WrapFPABool:
            Qlearning.setStrategy(WrapFPA)
            Qlearning.learn()
            Qlearning.save("wyniki/" + mapstr + "/WrapFPA.txt", mapa=False)
        if WrapWOABool:
            Qlearning.setStrategy(WrapWOA)
            Qlearning.learn()
            Qlearning.save("wyniki/" + mapstr + "/WrapWOA.txt", mapa=False)
        if RandBool:
            flag = True
            Qlearning.setStrategy(RandInit)
            tests = 0
            while flag:
                Qlearning.learn()
                tests += 1
                if (
                    Qlearning.path
                    and Qlearning.pathLenght != 100
                    and Qlearning.pathSmoothness != 100
                ):
                    flag = False
            print(f"That took {tests} tries")
            Qlearning.save("wyniki/" + mapstr + "/RandInit.txt", mapa=False)


Qlearning.createMap(-1)
genForMap(Qlearning, "map1")
Qlearning.createMap(0)
genForMap(Qlearning, "map2")
Qlearning.createMap(1)
genForMap(Qlearning, "map3")
Qlearning.createMap(2)
genForMap(Qlearning, "map4")
Qlearning.createMap(3)
genForMap(Qlearning, "map5")
MapStrings = [
    "randMap/rand1",
    "randMap/rand2",
    "randMap/rand3",
    "randMap/rand4",
    "randMap/rand5",
]
for mapstr in MapStrings:
    RecMap = reconstructMap(mapstr)
    Qlearning.setMap(RecMap)
    genForMap(Qlearning, mapstr)
# Qlearning.createMap(4)
# genForMap(Qlearning, "randMap/rand1")
# Qlearning.createMap(4)
# genForMap(Qlearning, "randMap/rand2")
# Qlearning.createMap(4)
# genForMap(Qlearning, "randMap/rand3")
# Qlearning.createMap(4)
# genForMap(Qlearning, "randMap/rand4")
# Qlearning.createMap(4)
# genForMap(Qlearning, "randMap/rand5")
