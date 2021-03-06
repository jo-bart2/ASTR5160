import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table, vstack
from astropy.coordinates import SkyCoord
import astropy.units as u
from sklearn import neighbors
from tasks.week8.class16 import coords_from_sweep, sweep_files
from tasks.week10.class18 import flux_to_mag
from tasks.week11.class19 import sweep_index
from tasks.week13.class23 import linear
from homeworks.hw4 import sweep_paths

# JAB Functions to 'train' the identifier
def qso_color_cuts(qso, star, testdata):
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
    s_mg = flux_to_mag(np.array(star['FLUX_G'][star['FLUX_G'] > 0]))
    q_mg = flux_to_mag(np.array(qso['FLUX_G'][qso['FLUX_G'] > 0]))
    s_mr = flux_to_mag(np.array(star['FLUX_R'][star['FLUX_R'] > 0]))
    q_mr = flux_to_mag(np.array(qso['FLUX_R'][qso['FLUX_R'] > 0]))
    s_mz = flux_to_mag(np.array(star['FLUX_Z'][star['FLUX_Z'] > 0]))
    q_mz = flux_to_mag(np.array(qso['FLUX_Z'][qso['FLUX_Z'] > 0]))
    s_w1 = flux_to_mag(np.array(star['FLUX_W1'][star['FLUX_W1'] > 0]))
    q_w1 = flux_to_mag(np.array(qso['FLUX_W1'][qso['FLUX_W1'] > 0]))
    
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
    s_data = np.array([[s_gz[i], s_rw[i]] for i in range(len(s_gz))])
    q_data = np.array([[q_gz[i], q_rw[i]] for i in range(len(q_gz))])

    t_data = np.array([[t_gz[i], t_rw[i]] for i in range(len(t_gz))])

    # JAB Make "known" data arrays
    data = np.concatenate([s_data, q_data])
    data_class = np.concatenate([np.zeros(len(s_data), dtype='i'), 
                                 np.ones(len(q_data), dtype='i')])
    target_names = np.array(['star', 'QSO'])

    # JAB Use k-NN to determine if objects are stars or qsos
    knn = neighbors.KNeighborsClassifier(n_neighbors=1)
    knn.fit(data, data_class)


    predicted_class = np.array(knn.predict(t_data))
    
    return predicted_class, s_data, q_data, t_data

def plot_classified(predicted_class, s_data, q_data, t_data, m, b):
    t_stars = t_data[predicted_class == 0]
    t_qsos = t_data[predicted_class == 1]

    starsx = np.array([s_data[i][0] for i in range(len(s_data))])
    starsy = np.array([s_data[i][1] for i in range(len(s_data))])

    qsox = np.array([q_data[i][0] for i in range(len(q_data))])
    qsoy = np.array([q_data[i][1] for i in range(len(q_data))])

    line = linear(m, starsx, b)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(starsx, starsy, color='r', label='stars')
    ax.scatter(qsox, qsoy, color='c', label='quasars')
    ax.plot(starsx, line, color='k')
    for i in range(len(t_stars)):
        ax.scatter(t_stars[i][0], t_stars[i][1], color='r', marker='*')
    for i in range(len(t_qsos)):
        ax.scatter(t_qsos[i][0], t_qsos[i][1], color='c', marker='*')

    ax.set_xlabel('g-z')
    ax.set_ylabel('r-W1')
    ax.legend()
    plt.show()


if __name__ == '__main__':
    # JAB Code for 'training' the classifications with proper cuts
    qsopath = '/d/scratch/ASTR5160/week10/qsos-ra180-dec30-rad3.fits'
    qsos = Table.read(qsopath)

    dirpath = '/d/scratch/ASTR5160/data/legacysurvey/dr9/south/sweep/9.0'
    sweeppath = sweep_paths(dirpath, qsos['RA'], qsos['DEC'])

    # JAB Cross match sweep files and limit to criteria (PSF, r<19)
    objs_list = []
    for p in sweeppath:
        objs_all = Table.read(p)
        
        mr = flux_to_mag(objs_all['FLUX_R'])
        
        ii_p = (objs_all['TYPE'] == 'PSF') & (mr < 19)

        objs_list.append(objs_all[ii_p])
    
    objs = vstack(objs_list)

    # JAB Create list of 'stars' and qsos for the 'known' data
    iiq = sweep_index(qsos['RA'], qsos['DEC'], objs, 0.5, u.arcsec)
    qsos = objs[iiq]
    qsos = qsos[flux_to_mag(qsos['FLUX_R']) < 19]

    star_index = np.random.randint(0,len(objs),len(qsos))
    stars = vstack([objs[i] for i in star_index])

    # JAB Use funtion to test a few objects
    test = objs[0:61]
    pclass, s_data, q_data, t_data = qso_color_cuts(qsos, stars, test)
    plot_classified(pclass, s_data, q_data, t_data, 1, -1.1)
