#!/usr/bin/env python3
from ev3dev2.motor import MediumMotor, OUTPUT_B
from time import sleep

def main():
    mot = MediumMotor(OUTPUT_B)
    deg = 1
    while True:
        mot.on_for_degrees(speed=20, degrees=deg)
        sleep(0.5)

if __name__=="__main__":
    main()