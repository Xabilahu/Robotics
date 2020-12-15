#!/usr/bin/env python3

'''
0 1 2 3 4 5 6 7
Left ---- Right
'''

from ev3dev2.sensor import Sensor, INPUT_2, INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveTank
from ev3dev2.led import Leds
from time import sleep
from threading import Thread
import os

leftSpeed = 20
rightSpeed = 20
lsa = Sensor(INPUT_2)
motor = MoveTank(OUTPUT_D, OUTPUT_A)
colorSensor = ColorSensor(INPUT_1)
threshold = 95
turning = False
baseSpeed = 10

PIZZA_DELIVERY = False
DELTA = 5

def reset_console():
    '''Resets the console to the default state'''
    print('\x1Bc', end='')

def set_cursor(state):
    '''Turn the cursor on or off'''
    if state:
        print('\x1B[?25h', end='')
    else:
        print('\x1B[?25l', end='')

def set_font(name):
    '''Sets the console font
    A full list of fonts can be found with `ls /usr/share/consolefonts`
    '''
    os.system('setfont ' + name)

def getLSA(lsa):
    values = []
    for i in range(0,8):
        values.append(lsa.value(i))
    return values

class Semaphore(Thread):
    '''
    2-Blue
    3-Green
    5-Red
    '''
    def __init__(self, threadID, semaphoreSequence):
        Thread.__init__(self)
        self.threadID = threadID
        self.running = True
        self.semaphoreSequence = semaphoreSequence
        self.currentSemaphore = 0
        self.currentLight = 0
        self.detectedSemaphore = False

    def run(self):
        global PIZZA_DELIVERY

        while self.running:
            color = colorSensor.color

            if color == 2: #Differentiate between blue and green
                _, _, b = colorSensor.rgb
                color = 2 if b > 60 else 3

            f = open('colors.csv', 'a')
            f.write("{}\n".format(color))
            f.close()

            if not self.detectedSemaphore:
                if color in [2, 3, 5]:
                    if self.semaphoreSequence[self.currentSemaphore][self.currentLight] == color:
                        self.currentLight += 1
                    
                    if self.currentLight == 3:
                        print('PIZZAAAAAA!')
                        self.detectedSemaphore = True
                        self.currentSemaphore += 1
                        self.currentLight = 0
                        PIZZA_DELIVERY = True

                sleep(0.05)
            else:
                sleep(2)
                PIZZA_DELIVERY = False
                self.detectedSemaphore = False


class FollowLine(Thread):
    def __init__(self, threadID):
        Thread.__init__(self)
        self.threadID = threadID
        self.running = True

    def run(self):
        global leftSpeed, rightSpeed
        while self.running:
            readings = getLSA(lsa)

            leftBlack = 1
            rightBlack = 1

            for i in range(len(readings)):
                if i <= 3 and readings[i] < threshold:
                    leftBlack += 1
                elif i >= 4 and readings[i] < threshold:
                    rightBlack += 1

            if (leftBlack < rightBlack): ## Turn Left
                turning = True
                leftSpeed = baseSpeed + 4 * leftBlack
                rightSpeed = baseSpeed + 8 * rightBlack
            elif (leftBlack > rightBlack): ## Turn Right
                turning = True
                leftSpeed = baseSpeed + 8 * leftBlack
                rightSpeed = baseSpeed + 4 * rightBlack
            else:
                if (leftBlack == 1 and turning):
                    pass
                else:
                    leftSpeed = rightSpeed = 20
                    turning = False
            sleep(0.05)

if __name__ == "__main__":
    reset_console()
    set_cursor(True)
    set_font('Lat15-Terminus12x6')
    line_follow = FollowLine(1)
    line_follow.setDaemon = True
    line_follow.running = True
    semaphore = Semaphore(2, [[3, 2, 5], [5, 3, 2], [2, 5, 3]])
    semaphore.setDaemon = True
    semaphore.running = True

    line_follow.start()
    semaphore.start()

    while True:
        if PIZZA_DELIVERY:
            DELTA += 1
            lSpeed = DELTA + leftSpeed
            rSpeed = rightSpeed - DELTA
            motor.on(0.5 * leftSpeed + 0.5 * lSpeed, 0.5 * rightSpeed + 0.5 * rSpeed)
        else:
            DELTA = 5
            motor.on(leftSpeed, rightSpeed)
        sleep(0.05)
