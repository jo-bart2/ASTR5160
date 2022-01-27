import numpy as np
from astropy.coordinates import SkyCoord
from astropy.time import Time

#JAB RA and Dec of the star Procyon
r = '07h39m18s' #RA
d = '+05d13m30s' #Dec

#JAB Convert RA and Dec to degrees
deg = SkyCoord(r,d,frame='icrs')
print(deg)
print('The RA and Dec of Procyon in degrees is ' + str(deg.ra.degree) + ', ' + str(deg.dec.degree))