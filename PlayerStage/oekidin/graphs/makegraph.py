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
plt.scatter(x, y, s=3, zorder=1)
plt.imshow(img, zorder=0, extent=[-8.0, 8.0, -8.0, 8.0], cmap='gray', vmin=0, vmax=1) #cave.png limits
plt.legend('Robotaren ibilbidea', scatterpoints=1)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Cave mapa')
#plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labeltop=False, labelleft=False, labelright=False)
plt.gca().legend().set_visible(False)
plt.show()
#base=os.path.basename(sys.argv[1])
#plt.savefig('results/'+os.path.splitext(base)[0])

