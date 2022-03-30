import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.coordinates import SkyCoord
import astropy.units as u
from tasks.week8.class16 import coords_from_sweep, sweep_files

# JAB Make function to determine indices of objects in sweep files
def sweep_index(ra, dec, sweep_table, radius):
    '''
    Parameters
    ----------
    ra: :class: '~numpy.ndarray'
       An array containing the RAs of the objects to identify

    dec: :class: '~numpy.ndarray'
       An array containing the Decs of the objects to identify

    sweep_table: :class: 'astropy.Table'
       An astropy Table read in from the sweep file(s)

    radius: :class: 'int', 'float'
       The value of the radius in arcsec around which to search

    Results
    -------
    id2: :class: '~numpy.ndarray'
       An array containing the indices of the sweep table that correspond to
       the RAs and Decs given of the objects
    '''
    
    c1 = SkyCoord(ra, dec, frame='icrs', unit='deg')
    c2 = SkyCoord(sweep_table['RA'], sweep_table['DEC'], frame='icrs', unit='deg')
    id1, id2, d1, d2 = c2.search_around_sky(c1, radius*u.arcsec)

    return id2

if __name__ == '__main__':
    # JAB Problem 1
    # JAB Find the closest object in sweep files to (188.53667, 21.04572)
    ra = np.array([188.53667])
    dec = np.array([21.04572])

    dirpath = '/d/scratch/ASTR5160/data/legacysurvey/dr9/south/sweep/9.0'
    sweepname = sweep_files(ra, dec, dirpath)
    sweeppath = '{}/{}'.format(dirpath, sweepname[0])

    objs = Table.read(sweeppath)
    ii = sweep_index(ra, dec, objs, 0.05)
    
    # JAB Determine the type of object it is
    ob_type = objs['TYPE'][ii][0]
    print('The type of object is: {}'.format(ob_type))
    # JAB This is an extended object

    # JAB Problem 2
