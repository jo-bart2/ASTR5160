import numpy as np
from astropy.table import Table, vstack
from astropy.coordinates import SkyCoord
import astropy.units as u
from tasks.week11.class19 import sweep_index

if __name__ == '__main__':
    # JAB Footprint in circular region of theta = 3 at (163, 50)
    theta = 3
    ra_center = np.array([163])
    dec_center = np.array([50])

    # JAB Problem 1
    # JAB Determine which FIRST sources are in the survey
    first_path = '/d/scratch/ASTR5160/data/first/first_08jul16.fits'
    f_data = Table.read(first_path)

    f_match = sweep_index(ra_center, dec_center, f_data, 3, u.degree)
    f_in = f_data[f_match]
    
    
