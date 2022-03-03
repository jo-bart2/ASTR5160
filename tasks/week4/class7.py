import matplotlib.pyplot as plt
import numpy as np
from numpy.random import random

# JAB create random set of 10,000 points for ra and dec coordinates in radians
ra = 2*np.pi*(random(10000)-0.5)
dec = np.arcsin(1.-random(10000)*2.)

# JAB plot points on (x, y) grid
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.scatter(ra, dec, marker='o', color='purple', alpha=0.5)
ax1.set_xlabel('RA (radians)')
ax1.set_ylabel('Dec (radians)')
plt.show()
# JAB In this projection, there are more points along the equator, near Dec = 0, than there are near the poles (dec = +/- pi/2)

# JAB Plot the same points in an Aitoff projection
fig2 = plt.figure()
ax2 = fig2.add_subplot(111, projection='aitoff')
ax2.scatter(ra, dec, marker='o', color='goldenrod', s=0.7, alpha=0.5)
xlab = ['14h','16h','18h','20h','22h','0h','2h','4h','6h','8h','10h']
ax2.set_xticklabels(xlab, weight=800)
ax2.grid(color='b', linestyle='dashed', linewidth=1.5)
plt.show()

# JAB Plot the same points in a Lambert projection
fig3 = plt.figure()
ax3 = fig3.add_subplot(111, projection='lambert')
ax3.scatter(ra, dec, marker='o', color='forestgreen', s=0.7, alpha=0.5)
ax3.set_xticklabels(xlab, weight=800)
ax3.grid(color='b', linestyle='dashed', linewidth=1.5)
plt.show()


