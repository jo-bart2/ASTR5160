import numpy as np
from astropy.table import Table

# JAB Function to identify quasars in a Table
def splendid_function():
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


if __name__ == '__main__':
    filepath = '/d/scratch/ASTR5160/week10/qsos-ra180-dec30-rad3.fits'
    data = Table.read(filepath)

    print(len(data[0]))
