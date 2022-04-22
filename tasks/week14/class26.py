import numpy as np
from astropy.table import Table

if __name__ == '__main__':
    # JAB Problem 1
    # JAB Read in file and find mean and variance of each bin
    filepath = '/d/scratch/ASTR5160/week13/line.data'
    data = Table.read(filepath, format='ascii')
    
    x = np.linspace(0.5, 9.5, 10)
    mean = np.array([np.mean(data['col{}'.format(i)]) for i in range(1,11)])
    var = np.array([np.var(data['col{}'.format(i)], ddof=1) for i in range(1,11)])

    # Problem 2
    
