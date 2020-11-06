from __future__ import print_function
import numpy as np
import math
from playercpp import *
import cv2
import time
import sys, select, termios, tty
import threading
from threading import Thread
import signal

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------

q/z : increase/decrease only linear speed by 10%
o/p : increase/decrease only angular speed by 10%

anything else : stop

CTRL-C to quit

"""

speedBindings={
        'q':(0.1,0),
        'z':(-0.1, 0),
    }
turnBindings={
        'o':(0,0.1),
        'p':(0, -0.1),

    }
# Class for managing ctrl-c
class SIGINT_handler():
   def __init__(self):
      self.SIGINT = False

   def signal_handler(self, signal, frame):
      print("You pressed Ctrl-C")
      self.SIGINT = True

# Class for linear and angular vels      
class Twist:
   def __init__(self, vlinear = 0, wangular = 0):
      self.v = vlinear
      self.w = wangular
   def set(self, v, w):
      self.v = v
      self.w = w
   def printTwist(self):
    return "currently:\tspeed %s\tturn %s " % (self.v,self.w)

# Map class: size, scale and bitmap
class Map:   
   def __init__(self, rows=1000, cols=1000, scale=20):
      ''' constructor function
        '''
      self.maxXsize = cols
      self.maxYsize = rows
      self.scale = scale
      self.ox = cols/2
      self.oy = rows/2
      self.map = np.zeros((rows, cols, 3), np.uint8)
        
   def setObstacle(self, xpos, ypos, color):
      i = self.ox + xpos * self.scale
      j = self.oy + ypos * self.scale
      if i < 0 or i > self.maxXsize:
         print("Error. X size exceeded")
         return -1
      if j < 0 or j > self.maxYsize:
         print("Error. Y size exceeded")
         return -1
      # set obstacle at i,j
      self.map[i,j] = color
      return 1


def getKey(settings):
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def vels(speed,turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

# Keyboard teleop function will run as a thread
def teleop(twist):
   speed = twist.v
   turn = twist.w

   try:
       settings = termios.tcgetattr(sys.stdin)
       print(msg)
       print(vels(speed,turn))
       while(1):
          global exitFlag
          if exitFlag:
             break
          key = getKey(settings)
          if key in speedBindings.keys():
             speed = speed + speedBindings[key][0]
             turn = 0
          elif key in turnBindings.keys():
             turn = turn + turnBindings[key][1]
             
          else:
             speed = 0
             turn = 0
   
          print(vels(speed,turn))
          if (key == '\x03'):
             break
          speed = min(max(-1, speed), 1)
          turn = min(max(-0.5, turn), 0.5)
          twist.v = speed #*x
          twist.w = turn #*th
          print("Velocities: ", twist.v, twist.w)
          time.sleep(0.001)

   except Exception as e:
       print(e)
 
   finally:
       termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

# Mapping function will run as a thread       
def mapping(twist):
    mapa = Map()
    bezeroa = PlayerClient("localhost", 6665)
    laserra = LaserProxy(bezeroa, 0)
    robota = Position2dProxy(bezeroa, 0)
    color0 = (0, 0, 255)
    color1 = (255, 0, 0)
        
    try:
        cv2.imshow("Mapa", mapa.map)
        for i in range(0,10):
           bezeroa.Read()
        count = laserra.GetCount()
        print("Count=", count)
        while 1:
            global exitFlag
            if exitFlag:
               break
            bezeroa.Read();
            # Get Robot Pose
            rx = robota.GetXPos()
            ry = robota.GetYPos()
            rtheta = robota.GetYaw()
            mapa.setObstacle(lx, ly, color0)
            for i in range(0, count): 
                if laserra.GetRange(i) < laserra.GetMaxRange():
                    lx = rx
                    ly = ry
                    mapa.setObstacle(lx, ly, color1)
            cv2.imshow("Mapa", mapa.map)
            cv2.waitKey(1)
            time.sleep(0.001)

            robota.SetSpeed(twist.v, twist.w)
    except Exception as e:
        print(e)
            
    finally:
         cv2.destroyAllWindows()

def handler(signum, frame):
    print('You pressed Ctrl-C')
         
if __name__ == "__main__":
   # Create new threads
   exitFlag = 0
   handler = SIGINT_handler()
   signal.signal(signal.SIGINT, handler.signal_handler)
   twist = Twist(0.01, 0.0)
   th1 = Thread(target=mapping, args = (twist,))
   th1.start()
   th2 = Thread(target=teleop, args = (twist, ))
   th2.start()
   while True:
      if handler.SIGINT:
         exitFlag = 1
      time.sleep(0.25)
      
         
