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

print('The 4-array for the cap bounded by 5h in RA is: '+str(ra_cap('5h')))
