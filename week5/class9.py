import matplotlib.pyplot as plt
import numpy as np
from numpy.random import random
import healpy as hp

# JAB Problem 1
# JAB Generate set of 1000000 points on surface of a sphere
ra = 360.*(random(1000000))
dec = (180/np.pi)*np.arcsin(1.-random(1000000)*2.)

# JAB Problem 2
# JAB Determine which pixels have points within nside=1
pix = hp.ang2pix(1, ra, dec, lonlat=True) # JAB returns array of pixel numbers

# JAB Determine area of a pixel with nside=1
area = hp.nside2pixarea(1, degrees=True)
print('The area of one pixel is ' + str(area) + ' square degrees')

# JAB Problem 3
# JAB Print number of points in each pixel
hist = np.histogram(pix, bins=12)
print('The number of points in each pixel is: ' +str(hist[0]))
# JAB This output is consistent with pixels being equal area since there are approxiamtely equal numbers of points within each pixel

# JAB Problem 4
# JAB Determine points in pixel 2 and overplot
ra2, dec2 = ra[pix == 2], dec[pix == 2]
ra5, dec5 = ra[pix == 5], dec[pix == 5]
ra8, dec8 = ra[pix == 8], dec[pix == 8]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(ra, dec, marker='o', color='black', s=0.5, alpha=0.3)
ax.scatter(ra2, dec2, marker='o', color='purple', s=0.5, label='Pixel 2')
ax.scatter(ra5, dec5, marker='o', color='green', s=0.5, label='Pixel 5')
ax.scatter(ra8, dec8, marker='o', color='orange', s=0.5, label='Pixel 8')
ax.legend(loc='upper left')
ax.set_xlabel('RA (degrees)')
ax.set_ylabel('Dec (degrees)')
plt.show()
