import numpy as np
from astropy.table import Table
from astropy.coordinates import SkyCoord
import astropy.units as u
from tasks.week8.class16 import coords_from_sweep, sweep_files

# JAB Problem 1
# JAB Use UBVRI to ugriz transformations for g and z magnitudes
# JAB From provided info, the magnitudes of the star are:
v = 15.256 # V magnitude
bv = 0.873 # B-V magnitude
ri = 0.511 # R-I magnitude

# JAB Use Jester et al. (2005) transformations
r = v - 0.42*bv + 0.11
rz = 1.72*ri - 0.41

z = r - rz
g = v + 0.60*bv - 0.12

# JAB Compare magnitudes to those in SDSS Navigator
# JAB Star coordinates: (16:35:26, +09:47:53) = (248.8583, 9.7981)
g_nav = 15.70
z_nav = 14.55

print('The g magnitude is expected to be {} and is {} in SDSS'.format(g, g_nav))
print('The z magnitude is expected to be {} and is {} in SDSS'.format(z, z_nav))

# JAB Problem 2
# JAB Get fluxes from Legacy Survey sweep files
ra = np.array([248.8583])
dec = np.array([9.7981])

dir_path = '/d/scratch/ASTR5160/data/legacysurvey/dr9/south/sweep/9.0'
filename = sweep_files(ra, dec, dir_path)[0]
filepath = '{}/{}'.format(dir_path, filename)
table = Table.read(filepath)

c1 = SkyCoord(ra, dec, frame='icrs', unit='deg')
c2 = SkyCoord(table['RA'], table['DEC'], frame='icrs', unit='deg')
id1, id2, d2, d3 = c2.search_around_sky(c1, 1*u.arcsec)

gflux = table['FLUX_G'][id2][0]
rflux = table['FLUX_R'][id2][0]
zflux = table['FLUX_Z'][id2][0]

# JAB Convert fluxes to magnitudes
mg = 22.5 - 2.5*np.log10(gflux)
mr = 22.5 - 2.5*np.log10(rflux)
mz = 22.5 - 2.5*np.log10(zflux)

print('g = {} mag, r = {} mag, z = {} mag'.format(mg, mr, mz))
# JAB These values agree fairly well with the SDSS values

#



