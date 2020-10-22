#!/usr/bin/env python3

'''
0 1 2 3 4 5 6 7
Left ---- Right
'''

from ev3dev2.sensor import Sensor, INPUT_2 
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveTank
from time import sleep
import os

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

def main():
    lsa = Sensor(INPUT_2)
    motor = MoveTank(OUTPUT_D, OUTPUT_A)
    leftSpeed = rightSpeed = 20
    threshold = 95
    turning = False

    while True:
        readings = getLSA(lsa)
        # for i in range(len(readings)):
        #     if (readings[i] < 100 and i < 3): ## Turn Left
        #         leftSpeed -= 30 * (1 / (i + 1))
        #         rightSpeed += 30 * (1 / (i + 1))
        #         break
        #     elif (readings[i] < 100 and i >= 4): ## Turn Right
        #         leftSpeed += 30 * (1 / (i - 3))
        #         rightSpeed += 30 * (1 / (i - 3))
        #         break
        #     else: ## Keep straight
        #         leftSpeed = 30
        #         rightSpeed = 30
        #         break

        leftBlack = 1
        rightBlack = 1

        for i in range(len(readings)):
            if i <= 3 and readings[i] < threshold:
                leftBlack += 1
            elif i >= 4 and readings[i] < threshold:
                rightBlack += 1


        if (leftBlack < rightBlack): ## Turn Left
            turning = True
            leftSpeed = 10 + 4 * leftBlack
            rightSpeed = 10 + 8 * rightBlack
        elif (leftBlack > rightBlack): ## Turn Right
            turning = True
            leftSpeed = 10 + 8 * leftBlack
            rightSpeed = 10 + 4 * rightBlack
        # elif (leftBlack == rightBlack and leftBlack == 0): ## Keep straight
        #     motor.off()
        else:
            if (leftBlack == 1 and turning):
                pass
            else:
                leftSpeed = rightSpeed = 20
                turning = False

        motor.on(leftSpeed, rightSpeed)
        sleep(0.1)

        # f = open("sensors.txt", "a")
        # f.write('{},{},{},{},{},{},{},{}\t{},{}\t{},{}\n'.format(readings[0], readings[1], readings[2], readings[3], readings[4], readings[5], readings[6], readings[7], leftSpeed, rightSpeed, leftBlack, rightBlack))
        # f.close()


if __name__ == "__main__":
    reset_console()
    set_cursor(True)
    set_font('Lat15-Terminus12x6')
    main()