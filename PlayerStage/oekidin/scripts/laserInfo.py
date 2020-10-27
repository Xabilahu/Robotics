import numpy as np
import math
from playercpp import *



def main():

    bezeroa = PlayerClient("localhost", 6665)
    laserra = LaserProxy(bezeroa, 0)
    robota = Position2dProxy(bezeroa, 0)

    print(bezeroa)

    robota.SetMotorEnable(True)
    bezeroa.Read()
    bezeroa.Read()
    bezeroa.Read()
    bezeroa.Read()

    count = laserra.GetCount()

    print("Scan count: ", count)
    print("Scan resolution: ", laserra.GetScanRes())
    print("Range resolution: ", laserra.GetRangeRes())
    print("Max Range: ",  laserra.GetMaxRange())
    print("Max angle: " , laserra.GetMaxAngle())
    print("Min angle: " , laserra.GetMinAngle())
    print("-----------------------------------")

    while 1:
	bezeroa.Read();
        max = -1.0
        min = laserra.GetMaxRange()
        maxind = -1
        minind = -1
	for i in range(0, count):
            if laserra.GetRange(i) > max and laserra.GetRange(i) != laserra.GetMaxRange():
                max = laserra.GetRange(i)
                maxind = i
            if laserra.GetRange(i) < min:
                min = laserra.GetRange(i)
                minind = i
        print("Max Reading: %4f, Index: %d"%(max, maxind))
        print("Min Reading: %4f, Index: %d"%(min, minind))
        print("-----------------------------------------")
#	robota.SetSpeed(0, 0.2)

if __name__ == "__main__":
    main()
