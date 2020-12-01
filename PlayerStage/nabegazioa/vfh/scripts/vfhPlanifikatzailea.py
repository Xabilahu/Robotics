from __future__ import print_function
import numpy as np
import math as m
from playercpp import *
import sys
import time

def main():
    try:
        bezeroa = PlayerClient("localhost", 6665)
        planifikatzailea = PlannerProxy(bezeroa, 0)
        
        helb = [[4, 4, 0], [4, -1.5, 0], [-4.5, -3.5, 0], [4.5, 2, 0],[-4, 3, 0], [4, 4, 0]]
        gc = 0;
        oldgc = -1;

        while gc < 6:
	    bezeroa.Read()
	    if not oldgc == gc:
	        x = helb[gc][0]
	        y = helb[gc][1]
	        a = m.radians(helb[gc][2])
	        print("Helburu berria: %d (%.2f %.2f %.2f)\n"%(gc, x, y, a))
	        planifikatzailea.SetGoalPose(x, y, a)
	        time.sleep(2.0)
	        for i in range(0, 20):
	            bezeroa.Read()
	        if not planifikatzailea.GetPathValid():
		    print("Helburua ez da atzigarria.\n")
		    oldgc = gc
		    gc += 1
	        else:
		    print("Helburua zilegizkoa da. Helburu zenbakia = %d\n"%(gc))
		    oldgc = gc
	    if planifikatzailea.GetPathDone():
                print("ROBOTA %d. HELBURUAN: Robotaren posea: %f %f %f Helburua: %f %f %f\n"%(gc, planifikatzailea.GetPose().px, planifikatzailea.GetPose().py, m.degrees(planifikatzailea.GetPose().pa), planifikatzailea.GetGx(), planifikatzailea.GetGy(), m.degrees(planifikatzailea.GetGa())))
	        oldgc = gc
	        gc += 1
    except Exception as e:
        print(e)
#    finally:
        #hemen zerbait?
      
if __name__ == "__main__":
    main()

