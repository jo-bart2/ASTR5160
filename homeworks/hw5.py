import numpy as np
from astropy.table import Table, vstack
from astropy.coordinates import SkyCoord
import astropy.units as u
from sklearn import neighbors
from tasks.week8.class16 import coords_from_sweep, sweep_files
from tasks.week10.class18 import flux_to_mag
from tasks.week11.class19 import sweep_index
from homeworks.hw4 import sweep_paths

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



    return
    

if __name__ == '__main__':
