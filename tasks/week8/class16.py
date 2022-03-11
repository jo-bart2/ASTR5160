import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
import os

# JAB Problem 6
# JAB Write function to find boundaries from sweep file names
# - adapted from decode_sweep_name() function provided
def coords_from_sweep(filename):
    '''
    Parameters
    ----------
    filename: :class: 'string'
        The full path to the sweep file

    Returns
    -------
    bounds: :class: '~numpy.ndarray'
        An array containing the ra and dec boundaries of the sweep file
    
    '''
    # JAB parts from decode_sweep_name()
    # ADM extract just the file part of the name.
    filename = os.path.basename(filename)

    # ADM the RA/Dec edges.
    ramin, ramax = float(filename[6:9]), float(filename[14:17])
    decmin, decmax = float(filename[10:13]), float(filename[18:21])

    # ADM flip the signs on the DECs, if needed.
    if filename[9] == 'm':
        decmin *= -1
    if filename[17] == 'm':
        decmax *= -1

    bounds = np.array([ramin, ramax, decmin, decmax])
        
    return bounds

# JAB Write function to find all sweep files needed
# JAB In part taken from is_in_box() function provided
def sweep_files(ras, decs, filepath):
    '''
    Parameters
    ----------
    ras: :class: '~numpy.ndarray'
       An array of ra coordinates for the objects
    
    decs: :class: '~numpy.ndarray'
       An array of dec coordinates for the objects

    filepath: :class: 'string'
       The full path to the directory, not including the file name

    Returns
    -------
    files: :class: 'list'
       A list of the file names containing the ras and decs
    
    '''
    # JAB Create array of coordinate boxes based on file names
    # JAB Want to make rest of this more efficient - not sure how
    filenames = os.listdir(filepath)
    filenames = [i for i in filenames if i.endswith('.fits')]
    radecboxs = [[],[],[],[]]
    for i in filenames:
        radec = coords_from_sweep(i)
        for x in range(4):
            radecboxs[x].append(radec[x])
    
    # JAB The part of the code adapted from is_in_box()
    ramin, ramax, decmin, decmax = radecboxs

    ii = [(ras >= ramin[i]) & (ras < ramax[i])
          & (decs >= decmin[i]) & (decs < decmax[i]) for i in range(len(ramin))]

    # JAB Determine which files are necessary from ras and decs
    files = [filenames[i] for i in range(len(filenames)) if ii[i]]

    return files

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
    path = '/d/scratch/ASTR5160/data/legacysurvey/dr9/north/sweep/9.0'
    filelist = sweep_files(ra100, dec100, path)
    print(filelist)
    
