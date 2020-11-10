import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

x = []
y = []

with open(sys.argv[1],'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(float(row[0]))
        y.append(float(row[1]))

img = mpimg.imread('cave.png')
plt.scatter(x, y, s=1, zorder=1)
plt.imshow(img, zorder=0, extent=[-8.0, 8.0, -8.0, 8.0], cmap='gray', vmin=0, vmax=1) #cave.png limits
if (np.array_equal(x[-5:-1], x[-10:-6]) and np.array_equal(y[-5:-1], y[-10:-6])):
    plt.scatter(x[-1],y[-1],zorder=1,c='r')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Cave mapa')
#plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labeltop=False, labelleft=False, labelright=False)
base=os.path.basename(sys.argv[1])
plt.savefig('results/'+os.path.splitext(base)[0])

