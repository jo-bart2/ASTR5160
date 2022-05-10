import numpy as np
import matplotlib.pyplot as plt
import emcee
import corner
from astropy.table import Table
from tasks.week13.class23 import linear

# JAB Rewrite functions from class26.py
# JAB Separate function for the log prior
def log_prior(params, minmax):
    '''
    Parameters
    ----------
    params: :class: 'list', '~numpy.ndarray'
       An array or list of the values for the parameters of the function.
       Should always be of length 3, but first term is zero if linear

       Linear: m and b in the shape [0, m, b]
       Quadratic: a2, a1, and a0 in the shape [a2, a1, a0]

    minmax: :class: 'list', '~numpy.ndarray'
       An array or list of arrays determining the prior range of the params
       in the samer order as the params array.
       Example: shape of [[], [m_min, m_max], [b_min, b_max]] for linear

    Returns
    -------
    lnprior: :class: 'float'
       The value of the natural log of the prior
    '''
    a2, a1, a0 = params
    if a2 == 0:
        minmax[0] = np.array([-1, 1])

    a2_min, a2_max = minmax[0]
    a1_min, a1_max = minmax[1]
    a0_min, a0_max = minmax[2]

    if a2_min <= a2 <= a2_max and a1_min <= a1 <= a1_max and a0_min <= a0 <= a0_max:
        lnprior = 0.0
    else:
        lnprior = -np.inf

    return lnprior


# JAB Rewrite posterior probability function
def log_posterior(params, xs, ys, yerrs, minmax):
    '''
    Parameters
    ----------
    params: :class: 'list', '~numpy.ndarray'
       An array or list of the values for the parameters of the function.
       Should always be of length 3, but first term is zero if linear

       Linear: m and b in the shape [0, m, b]
       Quadratic: a2, a1, and a0 in the shape [a2, a1, a0]
    
    xs: :class: '~numpy.ndarray'
       An array of the x values of the data
    
    ys: :class: '~numpy.ndarray'
       An array of the y values of the data

    yerrs: :class: '~numpy.ndarray'
       An array of the errors of the data

    minmax: :class: 'list', '~numpy.ndarray'
       An array or list of arrays determining the prior range of the params
       in the samer order as the params array.
       Example: shape of [[], [m_min, m_max], [b_min, b_max]] for linear

    Returns
    -------
    lnpost: :class: 'float'
       The natural log the of the posterior probability
    '''
    # JAB Calculate the prior
    lnprior = log_prior(params, minmax)

    # JAB Calculate the predicted y values for the model
    a2, a1, a0 = params
    ymodel = linear(a1, xs, a0) + a2*(xs**2)

    # JAB Calculate the natural log of the likelihood
    lnlike = (-0.5)*sum(((ys - ymodel)**2)/(yerrs**2) + np.log(2*np.pi*(yerrs**2)))

    # JAB Calculate the natural log of the posterior probability
    lnpost = lnprior + lnlike

    return lnpost

if __name__ == '__main__':
    # JAB Read in data file
    filepath = '/d/scratch/ASTR5160/final/dataxy.fits'
    data = Table.read(filepath)

    x, y, yerr = data['x'], data['y'], data['yerr']

    # JAB Use emcee to find linear fit
    
    
