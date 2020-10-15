#!/usr/bin/env python3
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.led import Leds
from time import sleep
from ev3dev2.sensor import INPUT_4

def main():
    us = UltrasonicSensor(INPUT_4)
    leds = Leds()
    leds.all_off()
    while True:
        if us.distance_centimeters < 60: # cm
            leds.set_color("LEFT", "RED")
            leds.set_color("RIGHT", "RED")
        else:
            leds.set_color("LEFT", "GREEN")
            leds.set_color("RIGHT", "GREEN")
        sleep (0.01)
if __name__ == "__main__":
    main()