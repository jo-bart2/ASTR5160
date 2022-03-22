import numpy as np
from astropy.table import Table
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
gflux = table['FLUX_G'][]

#print(table['RA'])
print(gflux)






