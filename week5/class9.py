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


