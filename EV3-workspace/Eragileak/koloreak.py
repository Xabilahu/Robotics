#!/usr/bin/env python3
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1
from time import sleep

def main():
    eye = ColorSensor(INPUT_1)
    while True:
        print(eye.rgb)
        red = eye.rgb[0]
        green = eye.rgb[1]
        blue = eye.rgb[2]
        print("Red: "+str(red))
        print("Green: "+str(green))
        print("Blue: "+str(blue))
        print("------------------------\n")
        sleep(0.5)

def main2():
    eye = ColorSensor(INPUT_1)
    for i in range(0, 20):
        print(eye.color_name, eye.color)
        sleep(0.5)

if __name__ == "__main__":
    main()