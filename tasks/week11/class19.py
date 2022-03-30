import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table, vstack
from astropy.coordinates import SkyCoord
import astropy.units as u
from tasks.week8.class16 import coords_from_sweep, sweep_files
from tasks.week10.class18 import flux_to_mag

# JAB Make function to determine indices of objects in sweep files
def sweep_index(ra, dec, sweep_table, radius, units):
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
       The value of the radius in around which to search

    units: :class: 'astropy.units'
       An astropy.units value for the units of the radius
    
    Results
    -------
    id2: :class: '~numpy.ndarray'
       An array containing the indices of the sweep table that correspond to
       the RAs and Decs given of the objects
    '''
    
    c1 = SkyCoord(ra, dec, frame='icrs', unit='deg')
    c2 = SkyCoord(sweep_table['RA'], sweep_table['DEC'], frame='icrs', unit='deg')
    id1, id2, d1, d2 = c2.search_around_sky(c1, radius*units)

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
    ii = sweep_index(ra, dec, objs, 0.05, u.arcsec)
    
    # JAB Determine the type of object it is
    ob_type = objs['TYPE'][ii][0]
    print('The type of object is: {}'.format(ob_type))
    # JAB This is an extended object

    # JAB Problem 2
    maskg = objs['ALLMASK_G'][ii][0]
    maskr = objs['ALLMASK_R'][ii][0]
    maskz = objs['ALLMASK_Z'][ii][0]

    print('The bitmask values for g, r, and z are: {}, {}, and {}'.format(
        maskg, maskr, maskz))
    print('The object is saturated in all bands')
    # JAB The object does appear to be saturated, but it doesn't have the normal
    # look of a galaxy. Simbad says it is a 'Possible Blazar' which means that it
    # actually likely is a galaxy, but our view of it is straight on the AGN jet

    # JAB Problem 3
    # JAB Find sweep files of all objects within 3 deg of (180, 30)
    # JAB Make arrays of ra and dec between (177, 27) and (183, 33)
    # JAB Creates a square, but works fine to find sweep files
    ras = np.concatenate((np.arange(177, 183.5, 0.5), np.arange(177, 183.5, 0.5)))
    decs = np.concatenate((np.arange(27, 33.5, 0.5), np.flip(np.arange(27, 33.5, 0.5))))
    
    ra3 = np.array([180])
    dec3 = np.array([30])
    
    # JAB Find all the sweep files for these coordinates
    sweepname3 = sweep_files(ras, decs, dirpath)
    sweeppath3 = ['{}/{}'.format(dirpath, i) for i in sweepname3]
    
    objs_all = vstack([Table.read(i) for i in sweeppath3])
    
    # JAB Restrict to objects within 3 degrees 
    ii3 = sweep_index(ra3, dec3, objs_all, 3, u.deg)
    objs3 = objs_all[ii3]

    # JAB Pull out only stellar objects
    psfobjs = objs3[objs3['TYPE'] == 'PSF']

    # JAB Restrict to r < 20
    mr = flux_to_mag(psfobjs['FLUX_R']/psfobjs['MW_TRANSMISSION_R'])
    psfobjs20 = psfobjs[mr < 20]
    print(len(psfobjs20))
    
