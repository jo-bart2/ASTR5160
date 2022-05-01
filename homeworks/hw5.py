import numpy as np
from astropy.table import Table
from tasks.week10.class18 import flux_to_mag
from tasks.week13.class23 import linear

# JAB Function to identify quasars in a Table
def splendid_function(datatable):
    '''
    Parameters
    ----------
    datatable: :class: 'astropy Table'
       A Table of objects with same columns as sweep files

    Returns
    -------
    ii_sq: :class: '~numpy.ndarray'
       A Boolean array showing which objects in datatable are qsos
    '''
    # JAB Determine g, z, r, and W1 magnitudes then make g-z and r-W1
    r = flux_to_mag(np.array(datatable['FLUX_R']))
    g = flux_to_mag(np.array(datatable['FLUX_G']))
    z = flux_to_mag(np.array(datatable['FLUX_Z']))
    w1 = flux_to_mag(np.array(datatable['FLUX_W1']))

    gz = g - z
    rw = r - w1
    
    # JAB Classify as quasar or star based on the line determined before
    # JAB The line is of the form y = 1*x - 1.1 and the quasars have g-z > -1
    # JAB These cuts are based on previous machine learning classifications in
    # the file testhw5.py
    m = 1
    b = -1.1
    x = np.linspace(min(gz[np.isfinite(gz)]), max(gz[np.isfinite(gz)]), len(gz))
    line = linear(m, x, b)
    
    ii_sq = (rw > line) & (gz > -1) & (datatable['TYPE'] == 'PSF') & (datatable['FLUX_G'] > 0) & \
    (datatable['FLUX_Z'] > 0) & (datatable['FLUX_W1'] > 0) & (datatable['FLUX_R'] > 0) & (r < 19)

    return ii_sq
    
    

if __name__ == '__main__':
    table = Table.read('/d/scratch/ASTR5160/data/legacysurvey/dr9/south/sweep/9.0/sweep-180p030-190p035.fits')
    ii = splendid_function(table)
    print(ii)
    print(len(table[ii]))
