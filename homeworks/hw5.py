import numpy as np
from astropy.table import Table


if __name__ == '__main__':
    filepath = '/d/scratch/ASTR5160/week10/qsos-ra180-dec30-rad3.fits'
    data = Table.read(filepath)

    print(len(data[0]))
