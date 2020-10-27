from __future__ import print_function
import numpy as np
import math
from playercpp import *
import sys


def main():
    try:
        bezeroa = PlayerClient("localhost", 6665)
        laserra = LaserProxy(bezeroa, 0)
        robota = Position2dProxy(bezeroa, 0)
        # Fitxategiaren burukoa
#        outFile = open(robotposes.txt, "w");
#        outFile.write("# Robotaren (x, y) koordenatuak \n")


        robota.SetMotorEnable(True)
        for i in range(0, 10):
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
            
            ''' Laserraren irakurketak kudeatu 
                Robotaren abiadurak finkatu 
            '''
            rx = robota.GetXPos()
            ry = robota.GetYPos()
            outFile.write("%.2f %.2f \n"%(rx, ry))
	    robota.SetSpeed(0, 0.2)
    except Exception as e:
        print(e)
    finally:
        #outFile.close()

if __name__ == "__main__":
    main()
