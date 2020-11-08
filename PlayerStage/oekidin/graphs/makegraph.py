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
plt.imshow(img, zorder=0, extent=[-8.0, 8.0, -8.0, 8.0]) #cave.png limits
#plt.legend('Robotaren ibilbidea', scatterpoints=1)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Cave mapa')
#plt.show()
base=os.path.basename(sys.argv[1])
plt.savefig('results/'+os.path.splitext(base)[0])

