#!/usr/bin/env python3
from ev3dev2.sensor import Sensor, INPUT_2
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
    while True:
        readings = getLSA(lsa)
        for i in range(len(readings)):
            print('{}: {}'.format(i, readings[i]))
        print('-------------------------')
                
        sleep(0.1)

if __name__ == "__main__":
    reset_console()
    set_cursor(True)
    set_font('Lat15-Terminus12x6')
    main()