import numpy as np
from astropy.table import Table
from astropy.coordinates import SkyCoord
import astropy.units as u


# JAB Function to identify quasars in a Table
def splendid_function(datatable):
    '''
    Parameters
    ----------
    datatable: :class: 'astropy Table'
       A Table of objects with same columns as sweep files

    Returns
    -------
    ----: :class: '~numpy.ndarray'
       A Boolean array showing which objects in datatable are qsos
    '''
    # JAB Determine the 'known' stars and quasars
    qsopath = '/d/scratch/ASTR5160/week10/qsos-ra180-dec30-rad3.fits'
    qsos = Table.read(qsopath)

    

if __name__ == '__main__':
