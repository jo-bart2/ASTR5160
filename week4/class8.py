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
c3_10 = SkyCoord(ra3[id3], dec3[id3], frame='icrs')
c4_10 = SkyCoord(ra4[id4], dec4[id4], frame='icrs')

# JAB Overplot all points within 10' of each other a different color
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.scatter(c3.ra.degree, c3.dec.degree, marker='o', color='olive', alpha=0.5, label='Set 1')
ax1.scatter(c4.ra.degree, c4.dec.degree, marker='+', color='coral', alpha=0.5, label='Set 2')
ax1.scatter(c3_10.ra.degree, c3_10.dec.degree, marker='o', color='purple', label='Set 1 within 10')
ax1.scatter(c4_10.ra.degree, c4_10.dec.degree, marker='+', color='purple', label='Set 2 within 10')
ax1.legend()
ax1.set_xlabel('RA (degrees)')
ax1.set_ylabel('Dec (degrees)')
plt.show()

# JAB Combine data sets into one array
ra_tot = np.concatenate([ra3, ra4])
dec_tot = np.concatenate([dec3, dec4])
c_tot = SkyCoord(ra_tot, dec_tot, frame='icrs')

# JAB Plot again using same symbol and color
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.scatter(c_tot.ra.degree, c_tot.dec.degree, marker='o', color='darkorange',label='All Data')
ax2.legend()
ax2.set_xlabel('RA (degrees)')
ax2.set_ylabel('Dec (degrees)')
plt.show()

# JAB Set coordinates of spectroscopic plate of 1.8 deg radius at (2h20m5s, -0d6m12s)
ra_plate, dec_plate = ['2h20m5s'], ['-0d6m12s']
c_plate = SkyCoord(ra_plate, dec_plate, frame='icrs')

# JAB Find which objects in data set fall within spectroscopic plate
ii = c_plate.separation(c_tot) < 1.8*u.degree

ra_in = ra_tot[ii == True]
dec_in = dec_tot[ii == True]
c_in = SkyCoord(ra_in, dec_in, frame='icrs')

# JAB Overplot these points
fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
ax3.scatter(c_in.ra.degree, c_in.dec.degree, marker='o', color='purple', label='Data within Plate')
ax3.scatter(c_tot.ra.degree, c_tot.dec.degree, marker='o', color='darkorange',alpha=0.5, label='All Data')
ax3.legend()
ax3.set_xlabel('RA (degrees)')
ax3.set_ylabel('Dec (degrees)')
plt.show()
