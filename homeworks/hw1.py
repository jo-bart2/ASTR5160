import numpy as np
from astropy.coordinates import SkyCoord
from astropy.time import Time
import astropy.units as u
import pandas as pd

# JAB Read in the data from the file and separate into ra and dec
data = pd.read_csv('/Users/jobartlett/Documents/School/Spring 2022/Astro Techniques II/HW1quasarfile.txt', header=None)
# data = pd.read_csv('/d/scratch/ASTR5160/week4/HW1quasarfile.txt', header=None)

ra = []
dec = []
for i in data[0]:
    radec = i[0:2] + ' ' + i[2:4] + ' ' + i[4:9] + ' ' + i[9:12] + ' ' + i[12:14] + ' ' + i[14:18]
    radec = radec.split()
    ra.append(radec[0]+'h'+radec[1]+'m'+radec[2]+'s')
    dec = (radec[3]+'d'+radec[4]+'m'+radec[5]+'s')

# JAB 
