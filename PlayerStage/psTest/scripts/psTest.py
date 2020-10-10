import numpy as np
import math
from playercpp import *
from time import sleep


def main():

    bezeroa = PlayerClient("localhost", 6665)
    laserra = LaserProxy(bezeroa, 0)
    robota = Position2dProxy(bezeroa, 0)

    print(bezeroa)

    robota.SetMotorEnable(True)

    for i in range(0,10):
        bezeroa.Read()
    count = laserra.GetCount()

    while 1:
        bezeroa.Read()
        for i in range(0, count):
            print(i, "Reading: ", laserra.GetRange(i))
        print("-----------------------------------------")
        robota.SetSpeed(0, 0.2)
        sleep(0.1)
if __name__ == "__main__":
    main()
