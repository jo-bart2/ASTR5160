import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord

# JAB convert (ra1, dec1) = (263.75, -17.9) and (ra2, dec2) = (20h24m59.9s, 10d6m0s) to cartesian
ra1 = 263.75*u.degree
dec1 = -17.9*u.degree
ra2 = '20h24m59.9s'
dec2 = '10d6m0s'

c1 = SkyCoord(ra=ra1, dec=dec1, frame='icrs')
c2 = SkyCoord(ra=ra2, dec=dec2, frame='icrs')
c1.representation_type = 'cartesian'
c2.representation_type = 'cartesian'
xyz1 = [c1.x.value, c1.y.value, c1.z.value]
xyz2 = [c2.x.value, c2.y.value, c2.z.value]

# JAB use dot product to find angle between objects
dot = np.dot(xyz1,xyz2)
mag1 = np.linalg.norm(xyz1)
mag2 = np.linalg.norm(xyz2)
angle = np.rad2deg(np.arccos(dot/(mag1*mag2)))
print('The angle between the two objects is: ' + str(angle) + ' degrees')

# JAB use SkyCoord separation to check result


