import numpy as np
from astropy.coordinates import SkyCoord

# JAB Problem 1
# JAB Write a function for a spherical cap bounded by ra=5h
def ra_cap(ra):
    dec = '0d'
    h = 1
    
    c = SkyCoord(ra, dec, frame='icrs')
    c.representation_type = 'cartesian'

    cap = np.array([c.x.value, c.y.value, c.z.value, h])
    
    return cap

print(ra_cap('5h'))
