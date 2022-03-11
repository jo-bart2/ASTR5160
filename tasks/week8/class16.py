import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
import os

# JAB Problem 6
# JAB Write function to find all sweep files needed
def sweep_files(ras, decs):
    '''
    Parameters
    ----------
    ras: :class: '~numpy.ndarray'
       An array of ra coordinates
    
    decs: :class: '~numpy.ndarray'
        An array of dec coordinates

    Returns
    -------
    '''
    
    r_vals = np.array([round(i, -1) for i in ras])
    print(r_vals)

if __name__ == '__main__':

    # JAB Problem 1
    file_dir = '/d/scratch/ASTR5160/data/first/first_08jul16.fits'
    data = Table.read(file_dir)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(data['RA'], data['DEC'], color='forestgreen', s=0.1)
    ax.set_xlabel('RA (deg)'), ax.set_ylabel('Dec (deg)')
    plt.show()

    # JAB Problem 3
    # JAB Query SDSS for first 100 data points
    filename = 'file.txt'
    ra100 = np.array(data['RA'][0:101])
    dec100 = np.array(data['DEC'][0:101])
    ''' JAB Uncomment if you want to run this, but it takes a long time
    if os.path.exists(filename):
        os.remove(filename) # JAB Remove old file
    for i in range(len(ra100)):
        os.system('python sdssDR9query.py {} {} >> {}'.format(ra100[i], dec100[i], 
                                                               filename))
    '''

    # JAB Problem 6
    # JAB Find files for first 100 data points
    sweep_files(ra100, dec100)
    
