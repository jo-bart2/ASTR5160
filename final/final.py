import numpy as np
import matplotlib.pyplot as plt
import emcee
import corner
from astropy.table import Table

if __name__ == '__main__':
    # JAB Read in data file and find mean and variance
    filepath = '/d/scratch/ASTR5160/final/dataxy.fits'
    data = Table.read(filepath)

    x, y, yerr = data['x'], data['y'], data['yerr']
    mean = np.mean(y)
    var = np.var(y, ddof=1)

    
    
