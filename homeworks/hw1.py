import numpy as np
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
from astropy.table import Table
import astropy.units as u
import argparse

# JAB Read in the data from the file and separate into ra and dec
#data = Table.read('/d/scratch/ASTR5160/week4/HW1quasarfile.txt', format='ascii.no_header')
data = Table.read('/Users/jobartlett/Documents/School/Spring 2022/Astro Techniques II/HW1quasarfile.txt', format='ascii.no_header')

ras = []
decs = []
c = []
for i in data['col1']:
    radec = i[0:2] + ' ' + i[2:4] + ' ' + i[4:9] + ' ' + i[9:12] + ' ' + i[12:14] + ' ' + i[14:18]
    radec = radec.split()
    ra, dec = radec[0]+'h'+radec[1]+'m'+radec[2]+'s', radec[3]+'d'+radec[4]+'m'+radec[5]+'s'

    coor = SkyCoord(ra, dec, frame='icrs')
    c.append(coor)

    ras.append(coor.ra.deg)
    decs.append(coor.dec.deg)

# JAB Determine time and location
kitt = EarthLocation.of_site('kpno')
utcoffset = -7*u.hour

parser = argparse.ArgumentParser()
parser.add_argument('month')
args = parser.parse_args()
m = args.month

if  m=='1' or m=='3' or m=='5' or m=='7' or m=='8' or m=='10' or m=='12':
    days = range(1,32)
elif m=='4' or m=='6' or m=='9' or m=='11':
    days = range(1,31)
elif m=='2':
    days = range(1,29)

times = ['2022-' + m + '-' + str(d) + ' 23:00:00' for d in days]
dates = Time(times, format='iso') - utcoffset

# JAB 


