import numpy as np
import matplotlib.pyplot as plt
import pymangle
from astropy.coordinates import SkyCoord
from numpy.random import random
from tasks.week6.class11 import circle_cap, write_ply

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

    return cap

# JAB Function to make a lat-lon rectangle of caps
def rect_caps(rmin, rmax, dmin, dmax):
    '''
    Parameters
    ----------
    rmin: :class: 'string'
       A string representing the minimum RA in the format hms

    rmax: :class: 'string'
       A string representing the maximum RA in the format hms

    dmin: :class: 'int' or 'float'
       A value for the minimum Dec bound in degrees

    dmax: :class: 'int' or 'float'
       A value for the maximum Dec bound in degrees
    
    Returns
    -------
    caps: :class: '~numpy.ndarray'
       An array of arrays containing the x,y,z, and h values for all four caps
    '''
    rcap_min = ra_cap(rmin)
    rcap_max = ra_cap(rmax, negative=True)
    dcap_min = dec_cap(dmin)
    dcap_max = dec_cap(dmax, negative=True)

    caps = np.array([rcap_min, rcap_max, dcap_min, dcap_max])

    return caps

if __name__ == '__main__':
    # JAB Problem 1
    # JAB The ras and decs to create the caps for the rectangle
    ramin = '10h15m'
    ramax = '11h15m'
    decmin = 30
    decmax = 40

    # JAB The coordinates of the plates
    plate_ra = np.array([155, 159, 163, 167])
    plate_dec = np.array([34, 36, 34, 36])
    theta = np.array([2, 2, 2, 2])

    # JAB Make caps for the lat-lon rectangle
    rect = rect_caps(ramin, ramax, decmin, decmax)
    
    # JAB Make the caps for the circular plates
    cc = circle_cap(plate_ra, plate_dec, theta)
    plates = np.array([[cc[0][i], cc[1][i], cc[2][i], cc[3][i]] for i in range(len(cc))])
    
    # JAB Create .ply file for the intersection of the plates and rectangle
    #caps = [[rect, i] for i in plates]
    caps = np.array([np.concatenate((rect, np.array([i]))) for i in plates])
    cp = np.array(['5', '5', '5', '5'])
    wt = np.array(['1', '1', '1', '1'])
    px = np.array(['0', '0', '0', '0'])
    st = np.array(['0', '0', '0', '0'])
    
    write_ply('survey', caps, cp, wt, px, st)

    # JAB Problem 2
    # JAB Create catalog of random points within the rectangle
    m = pymangle.Mangle('survey.ply')
    
    num = 10000000
    ra = 360.*(random(num))
    dec = (180/np.pi)*np.arcsin(1.-random(num)*2.)

    # JAB Find points within the mask
    good = m.contains(ra, dec)
    ra_in, dec_in = ra[good], dec[good]

    # JAB Determine area of the mask
    # JAB Divide number of points in mask by total number and multiply by total area of the sphere
    area_tot = 41252.96
    area_mask = (len(ra_in)/num)*area_tot
    print(area_mask)




    '''
    # JAB Plot points of each mask
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.scatter(ra, dec, color='purple', s=0.7)
    ax1.set_xlabel('RA (degrees)')
    ax1.set_ylabel('Dec (degrees)')
    plt.show()
    '''
