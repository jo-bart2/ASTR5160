import numpy as np
import matplotlib.pyplot as plt
import pymangle
from astropy.coordinates import SkyCoord
import os

# JAB Set up directory
user = os.getenv("USER")
formatter = "/d/www/jordan/public_html/week6"
webdir = formatter.format(user)

# JAB Problem 1
# JAB Use function from previous lecture
def circle_cap(ra, dec, theta):
    c = SkyCoord(ra, dec, frame='icrs', unit='deg')
    c.representation_type = 'cartesian'

    cap = np.array([c.x.value, c.y.value, c.z.value, 1-np.cos(np.deg2rad(theta))])

    return cap

# JAB Make two caps: theta=5 (76, 36) and theta=5 (75, 35)
cap1 = circle_cap(76, 36, 5)
cap2 = circle_cap(75, 35, 5)

# JAB Problem 2
# JAB Created .ply files manually in emacs

# JAB Problem 3
# JAB Read in each of the masks
minter = pymangle.Mangle("intersection.ply")
mboth = pymangle.Mangle("bothcaps.ply")

# JAB Fill each mask with 10000 random points
ra_inter, dec_inter = minter.genrand(10000)
ra_both, dec_both = mboth.genrand(10000)

# JAB Plot points of each mask
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.scatter(ra_inter, dec_inter, color='purple', label='Intersection Mask', s=0.7)
ax1.scatter(ra_both, dec_both, color='red', label='Both Mask', s=0.7)
ax1.legend()
ax1.set_xlabel('RA (degrees)')
ax1.set_ylabel('Dec (degrees)')
plt.show()
# JAB You can see one mask which includes both full caps and one that is only the intersection of the two

# JAB Problem 4
# JAB Flip the sign of constraint on cap1 and read in


