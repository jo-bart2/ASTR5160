import numpy as np
from astropy.table import Table
from astropy.coordinates import SkyCoord
import astropy.units as u
from tasks.week8.class16 import coords_from_sweep, sweep_files    

# JAB Function to convert fluxes to magnitudes
def flux_to_mag(fluxes):
    '''
    Parameters
    ----------
    fluxes: :class: '~numpy.ndarray'
       An array of fluxes to be converted (in units of nanomaggies)
    
    Returns
    -------
    mags: :class: '~numpy.ndarray'
       An array of magnitudes from the fluxes
    '''
    mags = 22.5 - 2.5*np.log10(fluxes)
    
    return mags

if __name__ == '__main__':
    # JAB Problem 1
    # JAB Read in star and qso files and make one list of ra and dec
    filepath = '/d/scratch/ASTR5160/week10/'
    starfile = 'stars-ra180-dec30-rad3.fits'
    qsofile = 'qsos-ra180-dec30-rad3.fits'
    stars = Table.read('{}{}'.format(filepath, starfile))
    qsos = Table.read('{}{}'.format(filepath, qsofile))

    radec = np.array([[*stars['RA'],*qsos['RA']], [*stars['DEC'],*qsos['DEC']]])

    # JAB Find sweep files containing correct objects
    dirpath = '/d/scratch/ASTR5160/data/legacysurvey/dr9/south/sweep/9.0'
    sweepnames = sweep_files(radec[0], radec[1], dirpath)
    sweeppaths = ['{}/{}'.format(dirpath, i) for i in sweepnames]
    
    # JAB Determine indeces of each object for the sweep files
    sweeps = np.concatenate(np.array([Table.read(i) for i in sweeppaths]))

    c1 = SkyCoord(radec[0], radec[1], frame='icrs', unit='deg')
    c2 = SkyCoord(sweeps['RA'], sweeps['DEC'], frame='icrs', unit='deg')
    id1, id2, d1, d2 = c2.search_around_sky(c1, 0.5*u.arcsec)
    
    # JAB Retrieve g, r, z, W1, and W2 fluxes from the sweeps
    gflux = sweeps['FLUX_G'][id2]
    rflux = sweeps['FLUX_R'][id2]
    zflux = sweeps['FLUX_Z'][id2]
    w1flux = sweeps['FLUX_W1'][id2]
    w2flux = sweeps['FLUX_W2'][id2]
    
    # JAB Problem 2
    # JAB Correct fluxes for galactic dust
    gflux_c = gflux/sweeps['MW_TRANSMISSION_G'][id2]
    rflux_c = rflux/sweeps['MW_TRANSMISSION_R'][id2]
    zflux_c = zflux/sweeps['MW_TRANSMISSION_Z'][id2]
    w1flux_c = w1flux/sweeps['MW_TRANSMISSION_W1'][id2]
    w2flux_c = w2flux/sweeps['MW_TRANSMISSION_W2'][id2]

    # JAB Convert fluxes to magnitudes
    mg = flux_to_mag(gflux_c)
    mr = flux_to_mag(rflux_c)
    mz = flux_to_mag(zflux_c)
    w1 = flux_to_mag(w1flux_c)
    w2 = flux_to_mag(w2flux_c)

    # JAB Problem 3




