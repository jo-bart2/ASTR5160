import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table

#JAB Read in the fits file
objs = Table.read("/d/scratch/ASTR5160/week2/struc.fits")

#JAB Determine lists of RA and DEC whose extinction is greater than 0.2
new_ra = objs["RA"][objs["EXTINCTION"][:,0] >0.2]
new_dec = objs["DEC"][objs["EXTINCTION"][:,0] >0.2]

#JAB Plot RA vs DEC and Overplot specific objects
plt.plot(objs["RA"],objs["DEC"],'o',alpha=0.5,label='All RA and DEC')
plt.plot(new_ra,new_dec,'x',color='red',label='Extinction > 0.2')
plt.xlabel('RA')
plt.ylabel('DEC')
plt.legend()
plt.show()

#JAB Create 3-array of random numbers
random1 = np.random.randint(0,101,100)
random2 = np.random.randint(0,101,100)
random3 = np.random.randint(0,101,100)

randomnum = np.array((random1,random2,random3))
print(randomnum)
print(randomnum[:,0])
#