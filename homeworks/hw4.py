import numpy as np
from astropy.table import Table, vstack
from astropy.coordinates import SkyCoord
import astropy.units as u
from tasks.week8.class16 import coords_from_sweep, sweep_files
from tasks.week10.class18 import flux_to_mag
from tasks.week11.class19 import sweep_index

def sweep_paths(directory, ras, decs):
    '''
    Parameters
    ----------
    directory: :class: 'string'
       A string containing the path to the directory of sweep files
    
    ras: :class: '~numpy.ndarray'
       An array of ra coordinates for the objects

    decs: :class: '~numpy.ndarray'
       An array of dec cooridnates for the objects

    Returns
    -------
    paths: :class: 'list'
       A list of strings representing the full paths to each sweep file

    '''
    names = sweep_files(ras, decs, directory)
    paths = ['{}/{}'.format(directory, i) for i in names]
    
    return paths

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
    
    # JAB Problem 2
    # JAB Find sweep files containing sources
    dirpath = '/d/scratch/ASTR5160/data/legacysurvey/dr9/north/sweep/9.0/'
    sweeppath = sweep_paths(dirpath, f_in['RA'], f_in['DEC'])

    # JAB Cross match sweep files and limit to criteria (PSF, r<22, W1-W2>0.5)
    objs_list = []
    for p in sweeppath:
        objs_all = Table.read(p)
        objs_match = objs_all[sweep_index(f_in['RA'], f_in['DEC'], 
                                          objs_all, 1, u.arcsec)]
        
        mr = flux_to_mag(objs_match['FLUX_R'])
        w1 = flux_to_mag(objs_match['FLUX_W1'])
        w2 = flux_to_mag(objs_match['FLUX_W2'])
        w12 = w1 - w2
        
        ii_p = (objs_match['TYPE'] == 'PSF') & (mr < 22) & (w12 > 0.5)

        objs_list.append(objs_match[ii_p])
    
    objs = vstack(objs_list)

    # JAB Problem 3
    # JAB Print out the total number of sources
    print('The total number of sources retrieved is: {}'.format(len(objs['RA'])))
