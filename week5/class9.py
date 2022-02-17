import matplotlib.pyplot as plt
import numpy as np
from numpy.random import random
import healpy as hp

# JAB Generate set of 1000000 points on surface of a sphere
ra = 360.*(random.(1000000))
dec = (180/np.pi)*np.arcsin(1.-random(1000000)*2.)

# JAB Determine which pixels have points within nside=1
