import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table

#JAB Read in the fits file
objs = Table.read("/d/scratch/ASTR5160/week2/struc.fits")

#JAB Determine lists of RA and DEC whose extinction is greater than 0.2
new_ra = objs["RA"][objs["EXTINCTION"][:,0] >=0.2]
new_dec = objs["DEC"][objs["EXTINCTION"][:,0] >=0.2]

#JAB Plot RA vs DEC and Overplot specific objects
plt.plot(objs["RA"],objs["DEC"],'o',label='All RA and DEC')
plt.xlabel('RA')
plt.ylabel('DEC')
plt.show()