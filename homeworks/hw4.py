import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table, vstack
from astropy.coordinates import SkyCoord
import astropy.units as u
from time import sleep
import argparse
from tasks.week8.class16 import coords_from_sweep, sweep_files
from tasks.week8 import sdssDR9query
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
    # JAB Find names of files and make string of full path
    names = sweep_files(ras, decs, directory)
    paths = ['{}/{}'.format(directory, i) for i in names]
    
    return paths

def sdss_mags(ra, dec):
    '''
    Much of this code comes directly from Adam's sdssDR9query.py

    Parameters
    ----------
    ra: :class: '~numpy.ndarray'
       An array of the RAs of the objects to query

    dec: :class: '~numpy.ndarray'
       An array of the Decs of the objects to query
    
    Returns
    -------
    u: :class: '~numpy.ndarray'
       An array of the returned u magnitudes from the query

    i: :class: '~numpy.ndarray'
       An array of the returned i magnitudes from the query
    
    ii: :class: 'boolean array'
       A boolean array for determining index of objects without u and i mags
    '''
    # ADM initialize the query.
    qry = sdssDR9query.sdssQuery()

    ui = []
    for radec in range(len(ra)):
        # ADM the query to be executed. You can substitute any query, here!
        # JAB Edited to only query for u and i magnitudes
        query = """SELECT top 1 u,i FROM PhotoObj as PT
        JOIN dbo.fGetNearbyObjEq(""" + str(ra[radec]) + """,""" + str(dec[radec]) + """,0.02) as GNOE
        on PT.objID = GNOE.objID ORDER BY GNOE.distance"""

        # ADM execute the query.
        qry.query = query
        for line in qry.executeQuery():
            result = line.strip()

        # ADM NEVER remove this line! It won't speed up your code, it will
        # ADM merely overwhelm the SDSS server (a denial-of-service attack)!
        sleep(1)

        # ADM the server returns a byte-type string. Convert it to a string.
        ui.append(result.decode())
    
    ui = np.array(ui)
    ii = ui != 'No objects have been found'
    ui_mags = ui[ii]
    
    # JAB Convert string to floats of ra and dec
    ui_list = [x.split(',') for x in ui_mags]
    u = np.array([float(x[0]) for x in ui_list])
    i = np.array([float(x[1]) for x in ui_list])
    
    return u, i, ii

def mag_to_flux(mags):
    '''
    Parameters
    ----------
    mags: :class: '~numpy.ndarray'
       An array of magnitudes to be converted
    
    Returns
    -------
    fluxes: :class: '~numpy.ndarray'
       An array of fluxes from the magnitudes (in nanomaggies)
    '''
    fluxes = 10**((22.5 - mags)/2.5)
    
    return fluxes

if __name__ == '__main__':
    # JAB Provide informative help message for module
    parser = argparse.ArgumentParser('Some help for the module')

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

    # JAB Problem 4
    # JAB Query SDSS and find u and i magnitudes
    umag, imag, ii_not = sdss_mags(objs['RA'], objs['DEC'])
    
    # JAB Problem 5
    # JAB Print total number of sources with SDSS matches
    print('The total number of SDSS sources is: {}'.format(len(umag)))

    # JAB Problem 6
    # JAB Remove FIRST sources with no SDSS match
    objs_sdss = objs[ii_not]
    
    # JAB Find brightest u-band source
    ii_brite = umag == min(umag)
    ubrite1 = objs_sdss[ii_brite]
    
    # JAB Problem 7
    # JAB Convert u and i magnitudes of ubrite1 to fluxes
    uflux = mag_to_flux(umag[ii_brite])
    iflux = mag_to_flux(imag[ii_brite])
    
    # JAB Problem 8
    # JAB Plot all of the fluxes as a function of wavelength
    fluxes = [uflux, ubrite1['FLUX_G'], ubrite1['FLUX_R'], iflux, ubrite1['FLUX_Z']
              , ubrite1['FLUX_W1'], ubrite1['FLUX_W2'], ubrite1['FLUX_W3'], 
              ubrite1['FLUX_W4']]
    
    waves = [0.3543, 0.4770, 0.6231, 0.7625, 0.9134, 3.4, 4.6, 12, 22]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(waves, fluxes, color='forestgreen')
    ax.plot(waves, fluxes, color='forestgreen', alpha=0.5)
    ax.set_xlabel('Wavelength (microns)')
    ax.set_ylabel('Flux (nanomaggies)')
    plt.show()
    
    # JAB Problem 9
    # JAB Examine ubrite1 in the SDSS Navigate Tool at (160.66714603364156, 48.56762346414696)

    # JAB Problem 10
    # JAB Comment on ubrite1 based on SDSS information
    print('Comments on ubrite1 based on information from the SDSS navigate tool:')
    print('The redshift of ubrite1 is 1.035. This is quite far for it to be a star\
 and still be the brightest object in the survey.')
    print('Instead, ubrite1 is classified on the Navigate Tool as a QSO.')
    print('This allows ubrite1 to be at a higher redshift, but still remain the brightest\
 object in the small survey.')
    print('The significant emission lines in the SDSS spectra and the strong peak at 22\
 micons in our data are further evidence of ubrite1 being a quasar.')
    
