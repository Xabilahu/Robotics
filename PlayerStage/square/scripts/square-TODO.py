from __future__ import print_function
import numpy as np
import math as m
from playercpp import *

import time
import sys, select, termios, tty

''' Helburua: odometria zer den landu eta dakarren errore metakorraz jabetu
    Hiru modu desberdinetara egin daiteke laukizuzena
    Ariketa gisa: hiru moduak zuzendu zehatzagoak izan daitezen trikimailuak
    erabiliz.
    Guztietan, errorea irudikatu grafika batean, posizioak denboran zehar jasoz
'''

## Time based distance and angle calculation
'''  Ariketa:
     side eta v, w-ren araberako denbora teorikoa kalkulatu
     zuzendu denborak laukizuzena zehatzagoa izateko
'''
def squareTime(v, w, side):
    filename = "../data/squareTime_s"+str(side)
    outFile = open(filename, "w")
    outFile.write("###  Parametroak: v: %.2f w: %.2f \n"%(v,w))
    outFile.write("#  Zutabeak: x y theta\n")
    print("Abiadurak: ", v, w)


    bezeroa = PlayerClient("localhost", 6665)
    robota = Position2dProxy(bezeroa, 0)
    x0 = robota.GetXPos()
    y0 = robota.GetYPos()
    theta0 = robota.GetYaw()

    try:
        while 1:
            bezeroa.Read()
            robota.SetSpeed(v, 0)
            time.sleep(1) # Aldatu balioa
            robota.SetSpeed(0, w)
            time.sleep(1) # Aldatu balioa
            outFile.write("%.2f %.2f %.2f\n "%(robota.GetXPos(), robota.GetYPos(), robota.GetYaw()))
            print("Robot pose: ", robota.GetXPos(), robota.GetYPos(), robota.GetYaw())

    except Exception as e:
        print(e)
    finally:
        outfile.close()

    
## Odom based distance and angle calculation
''' Ariketa gisa: +- errore marjina erabili azpihelburu bakoitzera
    heldu dela detektatzeko eta laukizuzena zehatzagoa egiteko
'''
def squareOdom(v, w, side):

    filename = "../data/squareOdom_s"+str(side)
    outFile = open(filename, "w")
    outFile.write("###  Parametroak: v: %.2f w: %.2f \n"%(v,w))
    outFile.write("#  Zutabeak: x y theta\n")
    bezeroa = PlayerClient("localhost", 6665)
    robota = Position2dProxy(bezeroa, 0)
    print("Abiadurak: ", v, w)
    for i in range(5):
        bezeroa.Read()
    x0 = robota.GetXPos()
    y0 = robota.GetYPos()
    dtheta = 0
    d = 0
    theta0 = robota.GetYaw()
    inside = True
    normdtheta = 0 
    try:
        while 1:
            bezeroa.Read()
            # Aldea irudikatzen
            if inside:
                robota.SetSpeed(v, 0)
                x = robota.GetXPos()
                y = robota.GetYPos()
                d = np.sqrt((x0 - x) * (x0 -x)+(y0 -y)*(y0-y))
                if d>=side:
                    inside = False
                    x0 = robota.GetXPos()
                    y0 = robota.GetYPos()
                    theta0 = robota.GetYaw()
            if not inside: # Biraketa
                robota.SetSpeed(0, 0) # Aldatu eta egokitu boraketa kontrolatzeko
                # ...
                
        outFile.write("%.2f %.2f %.2f\n "%(robota.GetXPos(), robota.GetYPos(), robota.GetYaw()))
                
    except Exception as e:
        print(e)
    finally:
        outfile.close()


''' 
       Posizio absolutuak eman behar zaizkio GoTo funtzioari
       Gainera, itxoin denbora finkatu behar da
       Ariketa gisa: odometriako balioak jaso ertz bakoitzean eta denboran zehar       metatzen den errorea aztertu, gps eta odom moduetan (.world fitxategia)  
'''

def squareGoto(side):

    filename = "../data/squareGoto_s"+str(side)
    outFile = open(filename, "w")
    outFile.write("#  Zutabeak: x y theta\n")

    bezeroa = PlayerClient("localhost", 6665)
    robota = Position2dProxy(bezeroa, 0)
    for i in range(5):
        bezeroa.Read()
    x0 = robota.GetXPos()
    y0 = robota.GetYPos()
    theta0 = robota.GetYaw()
    print("Initial pose: ", x0, y0, theta0)
    # Zuzen joan eta bira emateko denbora eman behar zaio
    t = 1
    try:
        while 1:
            '''
               Ertz bakoitzeko eskema hau errepikatu behar da
            '''
            bezeroa.Read()
            print("pose: ", robota.GetXPos(), robota.GetYPos(), robota.GetYaw())
            robota.GoTo(x0, y0, theta0)
            time.sleep(t)
            outFile.write("%.2f %.2f %.2f\n "%(robota.GetXPos(), robota.GetYPos(), robota.GetYaw()))
            print("Robot pose: ", robota.GetXPos(), robota.GetYPos(), robota.GetYaw())
            '''
               Eskema amaiera
            '''
            
    except Exception as e:
        print(e)
    finally:
        outfile.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Erabilera: python2.7 %s <v> <w> <d> <modua>"%(sys.argv[0]))
        print("    v: abiadura lineala (m/s)")
        print("    w: biraketa abiadura (rad/s)")
        print("    d: laukizuzenaren aldearen luzera (m)")
        print('    modua: 1 abiadura bidezko laukizuzena')
        print('           2 odometrian oinarritutako laukizuzena')
        print('           3 GoTo bidezko laukizuzena')
        exit(0)
    v = float(sys.argv[1])
    w = float(sys.argv[2])
    side = float(sys.argv[3])
    mode = int(sys.argv[4])
    if mode == 1:
        squareTime(v, w, side)
    if mode == 2:
        squareOdom(v, w, side)
    if mode == 3:
        squareGoto(side)
