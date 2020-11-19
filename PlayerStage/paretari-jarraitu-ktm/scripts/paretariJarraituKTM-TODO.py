from __future__ import print_function
import numpy as np
import math as m
from playercpp import *

import time
import sys, select, termios, tty
from sklearn.linear_model import LinearRegression


# PARAMETROAK ZEHAZTU 

LASER_IZPI_KOP = 180

def ktm(kp, filename):
    outFile = open(filename, "w");
    # Fitxategiaren burukoa
    outFile.write("###  Kp: %.2f\n"%(kp))
    outFile.write("# Angelua  c0 c1  w x y theta \n")

    bezeroa = PlayerClient("localhost", 6665)
    laserra = LaserProxy(bezeroa, 0)
    robota = Position2dProxy(bezeroa, 0)
        
    for i in range(0,10):
        bezeroa.Read()
    count = laserra.GetCount()
    try:
        while 1:
	    # Kalkulatu irakurketa "motzen" proiekzioak 
	    j = 0
            bezeroa.Read();
            xpos = np.zeros((count, 1), np.float)
            ypos = np.zeros((count, 1), np.float)
            for i in range(0, LASER_IZPI_KOP): #laserra.GetCount()):
                # Hemen laser izpiak proiektatu behar dira
                ypos[j] = 0
		xpos[j] = 0
                j = j+1
            if j>5:
	        # regresio lineala: karratu txikienen metodoa 
        	# KONTUZ!! j indizeak regresioa kalkulatzeko erabiliko den 
        	# puntu kopurua adierazten du!!  
                xpos.resize(j, 1)
                ypos.resize(j, 1)

	        model = LinearRegression()
                model.fit(ypos, xpos)
                c0 = float(model.intercept_)
                c1 = float(model.coef_)
	        #Kalkulatu robota eta paretaren arteko angelua */
	        print("# Zuzenaren ekuazioa: Y = c0 + c1*X = %g + %g X\n"%(c0, c1))
                # Angelua kalkulatu
                theta = 0
	        # Abiadurak finkatu
	        v = 0.0
                w = theta * kp 
                print("Abiadurak: ", v, w)
	        robota.SetSpeed(v, w);
	    outFile.write("%.2f %.2f %.2f %.2f %.2f %.2f %.2f\n "%(theta, c0, c1, w, robota.GetXPos(), robota.GetYPos(), robota.GetYaw()))
            time.sleep(0.02)

    except Exception as e:
        print(e)
    finally:
        outFile.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Erabilera: %s <Kp> [fitxategia]", sys.argv[0])
        exit(0)
    Kp = float(sys.argv[1])
    filename = "ktmOut.txt"
    if len(sys.argv) == 3:
        filename = sys.argv[2]
    ktm(Kp, filename)
