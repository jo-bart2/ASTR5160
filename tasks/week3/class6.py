import numpy as np
import matplotlib.pyplot as plt
import sfdmap
from astropy.coordinates import SkyCoord

#JAB The magnitudes of the first quasar, at (246.933, 40.795), are:
ugriz1 = np.array([18.82,18.81,18.73,18.82,18.90])

#JAB The magnitudes of the second quasar, at (236.562, 2.440), are:
ugriz2 = np.array([19.37,19.10,18.79,18.73,18.63])

#JAB plot uncorrected g-r vs r-i
plt.scatter(ugriz1[2]-ugriz1[3],ugriz1[1]-ugriz1[2],color='green',label='(246.933, 40.795)')
plt.scatter(ugriz2[2]-ugriz2[3],ugriz2[1]-ugriz2[2],color='purple',label='(236.562, 2.440)')
plt.legend()
plt.xlabel('r - i (mag)')
plt.ylabel('g - r (mag)')
plt.show()
# The two quasars are not very similar in color. The differences in r-i are only ~0.02, but \
    #the g-r values are off by more than 0.2 magnitudes.
#I feel like the colors should be similar if they are both similar quasars.

#JAB correct quasar magnitudes for extinction
dustdir = '/d/scratch/ASTR5160/data/dust/v0_1/maps'
m = sfdmap.SFDMap(dustdir, scaling=1)
ra1, dec1, ra2, dec2 = 246.933, 40.795, 236.562, 2.440
c1, c2 = SkyCoord(ra1, dec1, unit='deg'), SkyCoord(ra2, dec2, unit='deg')
ebv1, ebv2 = m.ebv(c1.ra.value,c1.dec.value), m.ebv(c2.ra.value,c2.dec.value)

ext1, ext2 = ebv1*ugriz1, ebv2*ugriz2

crct1, crct2 = ugriz1-ext1, ugriz2-ext2

plt.scatter(crct1[2]-crct1[3],crct1[1]-crct1[2],color='green',label='(246.933, 40.795)')
plt.scatter(crct2[2]-crct2[3],crct2[1]-crct2[2],color='purple',label='(236.562, 2.440)')
plt.legend()
plt.xlabel('Corrected r - i (mag)')
plt.ylabel('Corrected g - r (mag)')
plt.show()
#After the correction, the colors seem to have become slightly closer, but not to a significant extent

#JAB Visualizing the dust in the region of each quasar

#JAB Using meshgrid to create grids for each
x1, y1 = np.linspace(246.9-50*0.13,246.9+50*0.13,100), np.linspace(40.8-5,40.8+5,100)
x2, y2 = np.linspace(236.6-5,236.6+5,100), np.linspace(2.4-5,2.4+5,100)

xx1, yy1 = np.meshgrid(x1,y1)
xx2, yy2 = np.meshgrid(x2,y2)





