#!/usr/bin/env python3
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from time import sleep

def main():
    ts = TouchSensor()
    leds = Leds()
    leds.all_off()
    while True:
        if ts.is_pressed:
            leds.set_color('LEFT', "RED")
            leds.set_color("RIGHT", "RED")
        else:
            leds.set_color("LEFT", "GREEN")
            leds.set_color("RIGHT", "GREEN")
        sleep (0.01) # Give the CPU a rest
if __name__ == "__main__":
    main()