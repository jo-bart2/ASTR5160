import numpy as np
import matplotlib.pyplot as plt
import pymangle
from astropy.coordinates import SkyCoord

# JAB Function to create caps in RA (based on class12.py)
def ra_cap(ra, negative=False):
    '''
    Parameters
    ----------
    ra: :class: 'string'
       A string representing the RA in the format hms
    
    negative: :class: 'bool'
       A True or False to determine if the cap has a negative constraint
       The default is False

    Returns
    -------
    cap: :class: '~numpy.ndarray'
       An array of the x, y, z, and h values for the RA cap
    '''

    dec = '0d'
    h1 = 1
    
    if negative:
        h1 *= -1
    
    c = SkyCoord(ra, dec, frame='icrs')
    ra_new, dec_new = c.ra.degree+90, c.dec.degree
    c = SkyCoord(ra_new, dec, frame='icrs', unit='deg')
    c.representation_type = 'cartesian'

    cap = np.array([c.x.value, c.y.value, c.z.value, h1])
    
    return cap

# JAB Function for the caps in Dec (based on class12.py)
def dec_cap(dec, negative=False):
    '''
    Parameters
    ----------
    dec: :class: 'int' or 'float'
       A value for the Dec bound in degrees

    negative: :class: 'bool'
       A True or False to determine if the cap has a negative constraint
       The default is False
    
    Returns
    -------
    cap: :class: '~numpy.ndarray'
       An array of the x, y, z, and h values for the Dec cap
    '''
    c = SkyCoord(0, 90, frame='icrs', unit='deg')
    c.representation_type = 'cartesian'

    h = 1-np.sin(np.deg2rad(dec))
    if negative:
        h *= -1

    cap = np.array([c.x.value, c.y.value, c.z.value, h])

    return 
