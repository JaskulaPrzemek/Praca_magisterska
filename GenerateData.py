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
import gc

NNBool = True
WOABool = True
APFBool = True
FPABool = True
WrapFPABool = True
WrapWOABool = True
ZeroBool = True
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
    NN.load("NewTest/MseAdamNorm.keras")
    NN1 = n.NN()
    NN1.load("NewTest/MseAdamWrapW.keras")
    NN2 = n.NN()
    NN2.load("NewTest/MseAdamWrapF.keras")
if WrapFPABool:
    WrapFPA = weirdWrapper(flag=True)
if WrapWOABool:
    WrapWOA = weirdWrapper(flag=False)


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


MapStrings = ["map1", "map2", "map3", "map4", "map5"]
for index, map in enumerate(MapStrings):
    Qlearning.createMap(index - 1)
    genForMap(Qlearning, map)
    gc.collect()
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
    gc.collect()
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
