import numpy as np
import math
from playercpp import *
import time
import sys

laser_ang = 1
wmax = 0.1
wmin = -0.1
vmax = 0.3
vmin = 0.1


def main():
    filename = "outData.txt";
    bezeroa = PlayerClient("localhost", 6665)
    laserra = LaserProxy(bezeroa, 0)
    robota = Position2dProxy(bezeroa, 0)

    argc = len(sys.argv) # Numebr of arguments
    if (argc < 3):
        print("Robotak paretari jarraituko dio agindutako")
        print("distantzia mantenduz.")
        print("Erabilera: %s  <distantzia> <Kp> [<outFitx>] "%(sys.argv[0]))
        exit(0)
        
    dist = float(sys.argv[1])
    Kp = float(sys.argv[2])
    if argc == 4:
        filename = sys.argv[3]

    print("dist %f Kp %f fitx %s"%(dist, Kp, filename))
    datufitx = open(filename, "w")  
    
    print("Distantzia: %.2f Kp: %.2f outFilename: %s"%(dist, Kp, filename))
    # File header
    datufitx.write("## BatezbDist  Errorea  w v X Y\n")
    try:

        for i in range(0, 10):
	    bezeroa.Read()
        while 1:
	    batezbdist = 0
	    bezeroa.Read()
	    diff = 0
	    # Kalkulatu paretarako batezbesteko distantzia
	    # Kalkulatu errorea
            # Abiadurak finkatu proportzionalki
            w = 0
            v = 0
	    datufitx.write("%.2f %.2f %.2f %.2f %.2f %.2f\n"%(batezbdist, diff, w, v, robota.GetXPos(), robota.GetYPos()))
	    robota.SetSpeed(v, w)
            #time.sleep(0.02)
    except Exception as e:
        print(e)

    finally:
        datufitx.close()

if __name__ == "__main__":
    main()


