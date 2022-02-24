import numpy as np
import pymangle
from astropy.coordinates import SkyCoord
import os

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

