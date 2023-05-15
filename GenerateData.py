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

NNBool = False
WOABool = True
APFBool = True
FPABool = True
WrapFPABool = True
WrapWOABool = True
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
    NN.load("Models/16000/SqdModelMSEBig.keras")
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
            Qlearning.save("wyniki/" + mapstr + "/NN.txt", mapa=False)
        if WrapFPABool:
            Qlearning.setStrategy(WrapFPA)
            Qlearning.learn()
            Qlearning.save("wyniki/" + mapstr + "/WrapFPA.txt", mapa=False)
        if WrapWOABool:
            Qlearning.setStrategy(WrapWOA)
            Qlearning.learn()
            Qlearning.save("wyniki/" + mapstr + "/WrapWOA.txt", mapa=False)


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
Qlearning.createMap(4)
genForMap(Qlearning, "randMap/rand1")
Qlearning.createMap(4)
genForMap(Qlearning, "randMap/rand2")
Qlearning.createMap(4)
genForMap(Qlearning, "randMap/rand3")
Qlearning.createMap(4)
genForMap(Qlearning, "randMap/rand4")
Qlearning.createMap(4)
genForMap(Qlearning, "randMap/rand5")
