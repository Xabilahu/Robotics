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

if len(sys.argv) > 2 :
    img = mpimg.imread('hospital.png')
    ext = [-70, 70, -25, 25]
    plt.rc('font', size=4)
else:
    img = mpimg.imread('cave.png')
    ext = [-8.0, 8.0, -8.0, 8.0]
plt.scatter(x, y, s=0.1, zorder=1)
plt.imshow(img, zorder=0, extent=ext, cmap='gray', vmin=0, vmax=1) #cave.png limits
if (np.array_equal(x[-5:-1], x[-10:-6]) and np.array_equal(y[-5:-1], y[-10:-6])):
    plt.scatter(x[-1],y[-1],zorder=1,c='r')
plt.xlabel('x')
plt.ylabel('y')

if len(sys.argv) > 2 :
    plt.title('Ospital mapa')
else:
    plt.title('Cave mapa')

plt.tight_layout()
#plt.show()
#plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labeltop=False, labelleft=False, labelright=False)
base=os.path.basename(sys.argv[1])
plt.savefig('results/'+os.path.splitext(base)[0], dpi=500, bbox_inches='tight')

