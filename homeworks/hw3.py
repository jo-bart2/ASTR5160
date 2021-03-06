import numpy as np
from numpy.random import random
import matplotlib.pyplot as plt
import pymangle
import argparse
from astropy.coordinates import SkyCoord
from astropy.table import Table
from tasks.week6.class11 import circle_cap, write_ply
from homeworks.hw2 import field_area

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

# JAB Function to read in .dat file and separate into ra and dec
def radec_dat(filepath):
    '''
    Parameters
    ----------
    filepath: :class: 'string'
       A string representing the full path to the .dat file

    Returns
    -------
    ra_d: :class: '~numpy.ndarray'
       An array of the RAs in degrees

    dec_d: :class: '~numpy.ndarray'
       An array of the Decs in degrees
    '''
    # JAB Read in .dat file
    data = Table.read(filepath, format='ascii.no_header')

    # JAB separate into ra and dec from string
    ras = ['{}h{}m{}s'.format(i[0:2], i[2:4], i[4:9]) for i in data['col1']]
    decs = ['{}d{}m{}s'.format(i[9:12], i[12:14], i[14:18]) for i in data['col1']]
    
    c = SkyCoord(ras, decs, frame='icrs')

    ra_d, dec_d = np.array(c.ra.degree), np.array(c.dec.degree)

    return ra_d, dec_d

if __name__ == '__main__':
    # JAB Get input for directory to save figure to
    parser = argparse.ArgumentParser(
        'Make figure and save it to a particular directory')
    parser.add_argument('directory', help='The directory to save plot to')
    args = parser.parse_args()
    plot_dir = args.directory
    
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
    caps = np.array([np.concatenate((rect, np.array([i]))) for i in plates])
    cp = np.array(['5', '5', '5', '5'])
    wt = np.array(['1', '1', '1', '1'])
    px = np.array(['0', '0', '0', '0'])
    st = np.array(['0', '0', '0', '0'])
    
    write_ply('survey', caps, cp, wt, px, st)

    # JAB Problem 2
    # JAB Create catalog of random points within the rectangle
    write_ply('rectangle', [rect], ['4'], ['1'], ['0'], ['0'])

    mp = pymangle.Mangle('survey.ply')
    mr = pymangle.Mangle('rectangle.ply')

    num = 100000
    ra, dec = mr.genrand(num)

    # JAB Find points within the mask
    area_ii = mp.contains(ra, dec)
    ra_in, dec_in = ra[area_ii], dec[area_ii]

    # JAB Determine area of the mask
    # JAB Convert RAs to degrees for use in area function
    cmin = SkyCoord(ramin, '0d', frame='icrs')
    cmax = SkyCoord(ramax, '0d', frame='icrs')
    rmin_d, rmax_d = cmin.ra.degree, cmax.ra.degree

    # JAB Divide number of points in mask by total number in the rectangle then
    # multiply by the area of the rectangle
    area_tot = field_area(rmin_d, rmax_d, decmin, decmax)
    area_mask = (len(ra_in)/num)*area_tot
    
    # JAB Problem 3
    dat_path = '/d/scratch/ASTR5160/week8/HW3quasarfile.dat'

    # JAB Get the RAs and Decs of the quasars
    ra_q, dec_q = radec_dat(dat_path)

    # JAB Find the quasars inside the survey mask
    q_ii = mp.contains(ra_q, dec_q)
    ra_qin, dec_qin = ra_q[q_ii], dec_q[q_ii]

    # JAB Find the number density of quasars in the mask
    den = len(ra_qin)/area_mask

    # JAB Plot quasars inside and outside the mask
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(ra_q, dec_q, color='purple', s=0.7, alpha=0.4)
    ax.scatter(ra_qin, dec_qin, color='forestgreen', s=0.7)
    ax.text(155, 23, 'Mask Area = {} sqr deg'.format(round(area_mask,4)))
    ax.text(155, 20, 'Quasar Number Density = {} per sqr deg'.format(round(den,4)))
    ax.set_xlabel('RA (degrees)')
    ax.set_ylabel('Dec (degrees)')
    plt.savefig('{}/plot3.png'.format(plot_dir))

