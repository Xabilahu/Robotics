#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3Tire
from ev3dev2.unit import DistanceFeet

def main():
    STUD_MM = 8
    mdiff = MoveDifferential(OUTPUT_D, OUTPUT_A, EV3Tire, 16 * STUD_MM)
    robot = MoveSteering(OUTPUT_D, OUTPUT_A)
    mdiff.odometry_start(theta_degrees_start=0.0)
    mdiff.on_to_coordinates(SpeedRPM(40), 0, DistanceFeet(1).mm)
    mdiff.turn_to_angle(SpeedRPM(40), 90)
    mdiff.on_to_coordinates(SpeedRPM(40), DistanceFeet(1).mm, DistanceFeet(1).mm)
    mdiff.turn_to_angle(SpeedRPM(40), 90)
    mdiff.on_to_coordinates(SpeedRPM(40), DistanceFeet(1).mm, 0)
    mdiff.turn_to_angle(SpeedRPM(40), 90)
    mdiff.on_to_coordinates(SpeedRPM(40), 0, 0)
    mdiff.turn_to_angle(SpeedRPM(40), 90)
    print("Square finished")

if __name__=="__main__":
    main()