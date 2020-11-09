import matplotlib.pyplot as plt
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
import matplotlib.cbook as cbook
import os


x = []
y = []

with open(sys.argv[1],'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(float(row[0]))
        y.append(float(row[1]))



img = imread('cave.png')
plt.scatter(x,y,zorder=1)
if (np.array_equal(x[-5:-1], x[-10:-6]) and np.array_equal(y[-5:-1], y[-10:-6])):
    plt.scatter(x[-1],y[-1],zorder=1,c='r')
plt.imshow(img, zorder=0, extent=[-8.0, 8.0, -8.0, 8.0]) #cave.png limits
#plt.legend('Robotaren ibilbidea', scatterpoints=1)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Cave mapa')
#plt.show()
base=os.path.basename(sys.argv[1])
plt.savefig('results/'+os.path.splitext(base)[0])

