#!/usr/bin/env python3

'''
0 1 2 3 4 5 6 7
Left ---- Right
'''

from ev3dev2.sensor import Sensor, INPUT_2, INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveTank
from ev3dev2.sound import Sound
from time import sleep, time
from threading import Lock, Thread
import os

p = 0
i = 0
d = 0
kp = 0.5
ki = 0.05
kd = 0.125
readings = []
lsa = Sensor(INPUT_2)
motor = MoveTank(OUTPUT_D, OUTPUT_A)
colorSensor = ColorSensor(INPUT_1)
baseSpeed = 25
rightSpeed = baseSpeed
leftSpeed = baseSpeed
prevLeft = baseSpeed
prevRight = baseSpeed
mutex = Lock()

speed_history = []

PIZZA_DELIVERY = -1
INTERSECTION_DETECTED = False
SEMAPHORE_SEQ = [[3, 2, 5],
                 [5, 3, 2],
                 [2, 5, 3]]
ALPHA = 0.66

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
    for j in range(0,8):
        values.append(lsa.value(j))
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

            if not self.detectedSemaphore:
                if color in [2, 3, 5]:
                    if self.semaphoreSequence[self.currentSemaphore][self.currentLight] == color:
                        self.currentLight += 1
                    
                    if self.currentLight == 3:
                        PIZZA_DELIVERY = SEMAPHORE_SEQ.index(self.semaphoreSequence[self.currentSemaphore])
                        self.detectedSemaphore = True
                        self.currentSemaphore += 1
                        self.currentLight = 0

                sleep(0.25)
            else:
                sleep(30)
                PIZZA_DELIVERY = -1
                self.detectedSemaphore = False

class FollowLine(Thread):
    def __init__(self, threadID):
        Thread.__init__(self)
        self.threadID = threadID
        self.running = True
        self.sample_time = 0.01

    def run(self):
        global p, i, d, readings, INTERSECTION_DETECTED, mutex
        current_time = time()

        while self.running:
            mutex.acquire()
            readings = getLSA(lsa)
            right = sum(readings[:4])
            left = sum(readings[4:])

            INTERSECTION_DETECTED = right <= 300
            mutex.release()

            if not INTERSECTION_DETECTED:
            
                last_time = current_time
                current_time = time()
                delta_time = current_time - last_time

                if delta_time >= self.sample_time:
                    mutex.acquire()
                    last_p = p
                    p = right - left
                    i += p * delta_time
                    d = (p - last_p) / delta_time
                    mutex.release()

            sleep(0.01)

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
        if INTERSECTION_DETECTED and PIZZA_DELIVERY != -1:
            
            motor.off()
            
            first = True
            mutex.acquire()
            readings = getLSA(lsa)
            r = sum(readings[:4])
            l = sum(readings[4:])
            mutex.release()

            while first or (abs(r-l) > 50 and r < 350 and l < 350):
                mutex.acquire()
                readings = getLSA(lsa)
                r = sum(readings[:4])
                l = sum(readings[4:])
                mutex.release()
                motor.on(20, -20)
                print(PIZZA_DELIVERY)
                sleep(0.1 if not first else (2.15 if PIZZA_DELIVERY == 0 else (1 if PIZZA_DELIVERY == 1 else 0.5)))
                first = False

            INTERSECTION_DETECTED = False
            mutex.acquire()
            p = 0
            i = 0
            d = 0
            PIZZA_DELIVERY = -1
            mutex.release()
            continue
        else:
            line_follow.running = True
            mutex.acquire()
            error = kp * p + ki * i + kd * d
            mutex.release()
            prevRight = rightSpeed
            prevLeft = leftSpeed
            rightSpeed = baseSpeed + error
            leftSpeed = baseSpeed - error
        
        motor.on(max(min(60,ALPHA * leftSpeed + (1 - ALPHA) * prevLeft), -5),
                 max(min(60,ALPHA * rightSpeed + (1 - ALPHA) * prevRight), -5))

        sleep(0.01)
