import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u

# JAB Problem 1
# JAB Write a function for a spherical cap bounded by ra=5h
def ra_cap(ra):
    dec = '0d'
    h1 = 1
    
    c = SkyCoord(ra, dec, frame='icrs')
    ra_new, dec_new = c.ra.degree+90, c.dec.degree
    c = SkyCoord(ra_new, dec, frame='icrs', unit='deg')
    c.representation_type = 'cartesian'

    cap = np.array([c.x.value, c.y.value, c.z.value, h1])
    
    return cap

print('The 4-array for the cap bounded by 5h in RA is: ' + str(ra_cap('5h')))

# JAB Problem 2
# JAB Write function for spherical cap bounded by dec=36N
def dec_cap(dec):
    c = SkyCoord(0, 90, frame='icrs', unit='deg')
    c.representation_type = 'cartesian'

    cap = np.array([c.x.value, c.y.value, c.z.value, 1-np.sin(np.deg2rad(dec))])

    return cap

print('The 4-array for the cap bounded by 36N in dec is: ' + str(dec_cap(36)))

# JAB Problem 3
# JAB Write function for spherical cap for (5h, 36N) and theta=1
def field(ra, dec, theta):
    c = SkyCoord(ra, dec, frame='icrs')
    c.representation_type = 'cartesian'

    cap = np.array([c.x.value, c.y.value, c.z.value, 1-np.cos(np.deg2rad(theta))])

    return cap

print('The 4-array for the field bounded by (5h, 36N) is: ' + str(field('5h','36d',1)))
