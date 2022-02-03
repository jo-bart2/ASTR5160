import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord

#JAB RA and Dec of the star Procyon
r = '07h39m18s' #RA
d = '+05d13m30s' #Dec

#JAB Convert RA and Dec to cartesian with astropy
coords = SkyCoord(r,d,frame='icrs')
coords.representation_type = 'cartesian'
print('The coordinates of Procyon in cartesian are:')
print('x = ' + str(coords.x))
print('y = ' + str(coords.y))
print('z = ' + str(coords.z))