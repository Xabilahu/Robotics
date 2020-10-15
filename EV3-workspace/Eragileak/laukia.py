#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveTank
from time import sleep

def forward(tank, v, tsec):
    tank.on_for_seconds(v, v, seconds = tsec)

def turnLeft(tank, vl, vr, tsec):
    # turn left on the spot
    tank.on_for_seconds(vl, vr, seconds = tsec)

def main():
    # The MoveTank class provides the simplest way to drive two motors
    # left motor D
    # right motor A
    robot = MoveTank(OUTPUT_D, OUTPUT_A)
    for i in range(0, 4):
        forward(robot, 50, 3)
        sleep(0.5)
        turnLeft(robot, 20, -20, 1)
    print("Square finished")

if __name__=="__main__":
    main()