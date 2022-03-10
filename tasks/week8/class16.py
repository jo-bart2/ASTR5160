import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table

# JAB Problem 1
file_dir = '/d/scratch/ASTR5160/data/first/first_08jul16.fits'
data = Table.read(file_dir)
#print(data)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(data['RA'], data['DEC'], color='forestgreen', s=0.1)
ax.set_xlabel('RA (deg)'), ax.set_ylabel('Dec (deg)')
plt.show()
