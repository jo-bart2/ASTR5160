import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table, vstack
from astropy.coordinates import SkyCoord
import astropy.units as u
from tasks.week8.class16 import coords_from_sweep, sweep_files
from tasks.week10.class18 import flux_to_mag
from tasks.week11.class19 import sweep_index
from sklearn import neighbors

# JAB Function to classify star vs qso with machine learning
def ml_classify_objs(qso, star, testdata):
    '''
    Parameters
    ----------
    qso: :class: 'astropy.Table'
       An astropy table of quasars from a sweep file

    star: :class: 'astropy.Table'
       An astropy table of stars from a sweep file

    testdata: :class: 'astropy.Table'
       An astropy table of objects to be identified as a star or quasar

    Returns
    -------
    predicted_class: :class: '~numpy.ndarray'
       An array of 0 or 1 corresponding to star or quasar
    '''
    # JAB Determine color cuts of g-z and r-W1 for "known" data and input data
    s_mg, q_mg = flux_to_mag(np.array(star['FLUX_G'])), flux_to_mag(np.array(qso['FLUX_G']))
    s_mr, q_mr = flux_to_mag(np.array(star['FLUX_R'])), flux_to_mag(np.array(qso['FLUX_R']))
    s_mz, q_mz = flux_to_mag(np.array(star['FLUX_Z'])), flux_to_mag(np.array(qso['FLUX_Z']))
    s_w1, q_w1 = flux_to_mag(np.array(star['FLUX_W1'])), flux_to_mag(np.array(qso['FLUX_W1']))
    
    allmags = [s_mg, q_mg, s_mr, q_mr, s_mz, q_mz, s_w1, q_w1]
        
    s_gz, q_gz = allmags[0] - allmags[4], allmags[1] - allmags[5]
    s_rw, q_rw = allmags[2] - allmags[6], allmags[3] - allmags[7]
    
    t_mg = flux_to_mag(np.array(testdata['FLUX_G']))
    t_mr = flux_to_mag(np.array(testdata['FLUX_R']))
    t_mz = flux_to_mag(np.array(testdata['FLUX_Z']))
    t_w1 = flux_to_mag(np.array(testdata['FLUX_W1']))

    testmags = [t_mg, t_mr, t_mz, t_w1]

    t_gz = testmags[0] - testmags[2]
    t_rw = testmags[1] - testmags[3]

    # JAB Make data arrays for the color cuts
    s_data = np.array([[s_gz[i], s_rw[i]] for i in range(len(s_gz)) if 
                       np.isnan(s_gz[i]) == False and np.isnan(s_rw[i]) == False])
    q_data = np.array([[q_gz[i], q_rw[i]] for i in range(len(q_gz)) if 
                       np.isnan(q_gz[i]) == False and np.isnan(q_rw[i]) == False])

    t_data = np.array([[t_gz[i], t_rw[i]] for i in range(len(t_gz)) if 
                       np.isnan(t_gz[i]) == False and np.isnan(t_rw[i]) == False])

    # JAB Make "known" data arrays
    data = np.concatenate([s_data, q_data])
    data_class = np.concatenate([np.zeros(len(s_data), dtype='i'), 
                                 np.ones(len(q_data), dtype='i')])
    target_names = np.array(['star', 'QSO'])

    # JAB Use k-NN to determine if objects are stars or qsos
    knn = neighbors.KNeighborsClassifier(n_neighbors=1)
    knn.fit(data, data_class)

    predicted_class = np.array(knn.predict(t_data))
    
    return predicted_class

if __name__ == '__main__':
    # JAB Problem 2
    # JAB Recreate sample of quasars from class19.py
    # JAB Find sweep files of all objects within 3 deg of (180, 30)
    # JAB Make arrays of ra and dec between (177, 27) and (183, 33)
    # JAB Creates a square, but works fine to find sweep files
    ras = np.concatenate((np.arange(177, 183.5, 0.5), np.arange(177, 183.5, 0.5)))
    decs = np.concatenate((np.arange(27, 33.5, 0.5), np.flip(np.arange(27, 33.5, 0.5))))
    
    ra3 = np.array([180])
    dec3 = np.array([30])
    
    # JAB Find all the sweep files for these coordinates
    dirpath = '/d/scratch/ASTR5160/data/legacysurvey/dr9/south/sweep/9.0'
    sweepname3 = sweep_files(ras, decs, dirpath)
    sweeppath3 = ['{}/{}'.format(dirpath, i) for i in sweepname3]
    
    objs_all = vstack([Table.read(i) for i in sweeppath3])
    
    # JAB Restrict to objects within 3 degrees 
    ii3 = sweep_index(ra3, dec3, objs_all, 3, u.deg)
    objs3 = objs_all[ii3]

    # JAB Pull out only stellar objects
    psfobjs = objs3[objs3['TYPE'] == 'PSF']

    # JAB Restrict to r < 20
    mr = flux_to_mag(psfobjs['FLUX_R'])
    psfobjs20 = psfobjs[mr < 20]
    
    # JAB Coordinate match objects from qso file
    qsofile = '/d/scratch/ASTR5160/week10/qsos-ra180-dec30-rad3.fits'
    qobjs = Table.read(qsofile)

    iiq = sweep_index(qobjs['RA'], qobjs['DEC'], psfobjs20, 0.5, u.arcsec)
    qsos = psfobjs20[iiq]
    
    # JAB Problem 3
    # JAB Create list of 'stars' for the 'known' data
    star_index = np.random.randint(0,len(psfobjs20),len(qsos))
    stars = vstack([psfobjs20[i] for i in star_index])

    # JAB Use funtion to test a few objects
    test = psfobjs20[0:21]
    classes = ml_classify_objs(qsos, stars, test)
    
    
