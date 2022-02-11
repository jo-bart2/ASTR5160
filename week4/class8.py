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
sep = c1.separation(c2)
if round(sep.degree,6) == round(angle,6):
    print('The dot product and separation angles match')
else:
    print('The dot product and separation angles do not match')

# JAB populate the sky with 2 sets of 100 random points between ra = 2 and 3 and dec = -2 and 2
ra3, dec3 = (np.random.random(100)+2)*u.hour, ((np.random.random(100)*4)-2)*u.degree
ra4, dec4 = (np.random.random(100)+2)*u.hour, ((np.random.random(100)*4)-2)*u.degree
c3 = SkyCoord(ra3, dec3, frame='icrs')
c4 = SkyCoord(ra4, dec4, frame='icrs')

# JAB plot the two sets of points in different colors with different symbols
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(c3.ra.degree, c3.dec.degree, marker='o', color='olive', alpha=0.8, label='Set 1')
ax.scatter(c4.ra.degree, c4.dec.degree, marker='+', color='coral', label='Set 2')
ax.legend()
ax.set_xlabel('RA (degrees)')
ax.set_ylabel('Dec (degrees)')
plt.show()

# JAB Find all points within 10' of each other
id3, id4, d3, d4 = c4.search_around_sky(c3, (10./60)*u.degree)
c3_match = SkyCoord(ra3[id3], dec3[id3], frame='icrs')
c4_match = SkyCoord(ra4[id4], dec4[id4], frame='icrs')


