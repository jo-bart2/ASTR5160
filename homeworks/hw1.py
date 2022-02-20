import numpy as np
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.table import Table
import astropy.units as u

# JAB Read in the data from the file and separate into ra and dec
# data = pd.read_csv('/d/scratch/ASTR5160/week4/HW1quasarfile.txt', header=None)
data = Table.read('/Users/jobartlett/Documents/School/Spring 2022/Astro Techniques II/HW1quasarfile.txt', format='ascii.no_header')

ras = []
decs = []
c = []
for i in data['col1']:
    radec = i[0:2] + ' ' + i[2:4] + ' ' + i[4:9] + ' ' + i[9:12] + ' ' + i[12:14] + ' ' + i[14:18]
    radec = radec.split()
    ra, dec = radec[0]+'h'+radec[1]+'m'+radec[2]+'s', radec[3]+'d'+radec[4]+'m'+radec[5]+'s'
    ras.append(ra)
    decs.append(dec)

    c.append(SkyCoord(ra, dec, frame='icrs'))

# JAB 
