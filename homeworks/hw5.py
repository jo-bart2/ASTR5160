import numpy as np
from astropy.table import Table
import argparse
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
    # JAB Determine g, z, r, and W1 magnitudes for each object
    r = flux_to_mag(np.array(datatable['FLUX_R']))
    g = flux_to_mag(np.array(datatable['FLUX_G']))
    z = flux_to_mag(np.array(datatable['FLUX_Z']))
    w1 = flux_to_mag(np.array(datatable['FLUX_W1']))

    # JAB Calculate the color cuts for g-z and r-W1
    gz = g - z
    rw = r - w1
    
    # JAB Classify as quasar or star based on the line determined before
    # JAB The line is of the form y = 1*x - 1.1 and the quasars have g-z > -1
    # JAB These cuts are based on previous machine learning classifications in
    # the file testhw5.py
    m = 1
    b = -1.1
    line = linear(m, gz, b)
    
    ii_line = (rw > line) & (gz > -1)

    # JAB The objects should also be of type PSF and have r < 19
    ii_cuts = (datatable['TYPE'] == 'PSF') & (r < 19)

    ii_sq = ii_line & ii_cuts

    return ii_sq

if __name__ == '__main__':
    # JAB Provide informative help message and request file path
    parser = argparse.ArgumentParser('''This module completes the tasks put forth in Homework 5:
    It takes a path to a .fits file and prints the number of quasars present
    ''')
    parser.add_argument('filepath', help='The full path to the .fits file')
    args = parser.parse_args()
    filepath = args.filepath

    # JAB Reads in the .fits file
    table = Table.read(filepath)

    # JAB Finds the number of quasars present and prints it
    ii = splendid_function(table)
    qsos = table[ii]

    print('There are {} quasars present in the field'.format(len(qsos)))
    
