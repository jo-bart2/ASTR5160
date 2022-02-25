import numpy as np
import matplotlib.pyplot as plt
import pymangle
from astropy.coordinates import SkyCoord

# JAB Problem 1
# JAB Use ra_cap and dec_cap functions to make 4 caps with RA = 5h,6h and Dec = 30,40
def ra_cap(ra):
    dec = '0d'
    h1 = 1
    
    c = SkyCoord(ra, dec, frame='icrs')
    ra_new, dec_new = c.ra.degree+90, c.dec.degree
    c = SkyCoord(ra_new, dec, frame='icrs', unit='deg')
    c.representation_type = 'cartesian'

    cap = np.array([c.x.value, c.y.value, c.z.value, h1])
    
    return cap

def dec_cap(dec):
    c = SkyCoord(0, 90, frame='icrs', unit='deg')
    c.representation_type = 'cartesian'

    cap = np.array([c.x.value, c.y.value, c.z.value, 1-np.sin(np.deg2rad(dec))])

    return cap

cap5 = ra_cap('5h')
cap6 = ra_cap('6h')
cap30 = dec_cap(30)
cap40 = dec_cap(40)

# JAB Calculate area of rectangle in steradians


# JAB Write ply file with correct str and weight=0.9
def write_ply(name, cap, cp, wt, px, st):
    """
    Parameters
    ----------
    name : :class: 'string'
           The name of the file (without the .ply)
    cap : :class: '~numpy.ndarray'
          Array of arrays containing the xyz values and radius of each cap
    cp : :class: '~numpy.ndarray'
         Array of strings containing number of caps in each polygon
    wt : :class: '~numpy.ndarray'
         Array of strings of the weight of the polygons
    px : :class: '~numpy.ndarray'
         Array of string of the pixel number for the polygons
    st : :class: '~numpy.ndarray'
         Array of strings of the area of the polygons in steradians
    """

    # JAB Open file and write in lines
    file = open(name+'.ply', 'w')

    poly_num = len(cp) # JAB number of polygons
    line1 = '{} polygons\n'.format(poly_num)
    file.write(line1)

    # JAB loop through the number of polygons and the corresponding caps
    for i in range(poly_num):
        file.write('polygon {} ( {} caps, {} weight, {} pixel, {} str):\n'.format(i+1, cp[i], wt[i], px[i], st[i]))
        for j in cap[i]:
            file.write('  {} {} {} {}\n'.format(j[0], j[1], j[2], j[3]))
        
    file.close()


