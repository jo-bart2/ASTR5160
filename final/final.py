import numpy as np
import matplotlib.pyplot as plt
import emcee
import corner
from astropy.table import Table
from tasks.week13.class23 import linear
from tasks.week14.class26 import log_prior, log_posterior

# JAB Function that returns y value of quadratic
def quadratic(xs, a2, a1, a0):
    '''
    Parameters
    ----------
    xs: :class: '~numpy.ndarray', 'int', 'float'
       An array or single value for which to find the corresponding y

    a2: :class: 'int', 'float'
       The second order constant in the quadratic

    a1: :class: 'int', 'float'
       The first order constant in the quadtratic
    
    a0: :class: 'int', 'float'
       The zeroth order constant in the quadratic

    Returns
    -------
    y: :class: '~numpy.ndarray', 'int', 'float'
       An array or single value representing the output of the equation
       y = a2*x^2 + a1*x + a0
    '''
    y = a2*(xs**2) + a1*xs + a0

    return y

# JAB Rewrite prior and posterior functions for quadratic
def log_prior_quad(params, minmax):
    '''
    Parameters
    ----------
    params: :class: 'list', '~numpy.ndarray'
       An array or list of the three values for a2, a1, and a0 in the shape 
       of [a2, a1, a0]

    minmax: :class: 'list', '~numpy.ndarray'
       An array or list of arrays each containing the two values determining 
       the prior range of the params. Of the same length as params and in the 
       shape of [[a2_min, a2_max], [a1_min, a1_max], [a0_min, a0_max]]

    Returns
    -------
    lnprior: :class: 'float'
       The value of the natural log of the prior
    '''
    a2, a1, a0 = params
    
    a2_min, a2_max = minmax[0]
    a1_min, a1_max = minmax[1]
    a0_min, a0_max = minmax[2]

    if a2_min <= a2 <= a2_max and a1_min <= a1 <= a1_max and a0_min <= a0 <= a0_max:
        lnprior = 0.0
    else:
        lnprior = -np.inf

    return lnprior

def log_posterior_quad(params, xs, ys, yerrs, minmax):
    '''
    Parameters
    ----------
    params: :class: 'list', '~numpy.ndarray'
       An array or list of the three values for a2, a1, and a0 in the shape 
       of [a2, a1, a0]

    xs: :class: '~numpy.ndarray'
       An array of the x values of the data
    
    ys: :class: '~numpy.ndarray'
       An array of the y values of the data

    yerrs: :class: '~numpy.ndarray'
       An array of the errors in y of the data
    
    minmax: :class: 'list', '~numpy.ndarray'
       An array or list of arrays each containing the two values determining 
       the prior range of the params. Of the same length as params and in the 
       shape of [[a2_min, a2_max], [a1_min, a1_max], [a0_min, a0_max]]

    Returns
    -------
    lnpost: :class: 'float'
       The natural log the of the posterior probability
    '''
    a2, a1, a0 = params
    lnprior = log_prior_quad(params, minmax)

    # JAB Calculate the predicted y values for the model
    ymodel = quadratic(xs, a2, a1, a0)

    # JAB Calculate the natural log of the likelihood
    lnlike = (-0.5)*sum(((ys - ymodel)**2)/(yerrs**2) + np.log(2*np.pi*(yerrs**2)))

    # JAB Calculate the natural log of the posterior probability
    lnpost = lnprior + lnlike

    return lnpost

def use_emcee(starts, post, args, labels, steps=False, truths=None):
    '''
    Parameters
    ----------
    starts: :class: '~numpy.ndarray', 'list'
       Array or list of starting values of the parameters

    post: :class: 'function'
       The function for the posterior that will be fed in to the EnsembleSampler

    args: :class: 'tuple'
       A tuple containing the arguments other than the starting values to be 
       entered into the posterior function.
       Example: (xs, ys, var, mminmax, bminmax) for log_posterior

    labels: :class: '~numpy.ndarray', 'list'
       Array or list containing strings with the names of the parameters

    steps: :class: 'Boolean'
       A boolean to determine whether or not to plot the steps and parameters.
       Default is False

    truths: :class: '~numpy.ndarray', 'list'
       Array or list with the true values of the parameters, if known

    Returns
    -------
    fits: :class: 'list'
       A list of lists containing the best fit parameters in the form of
       [param name, best value, lower bound, upper bound]
    '''
    # JAB Run emcee based on tutorial and Class 26
    nparams = len(starts)
    pos = np.array([m_start, b_start]) + 1e-4 * np.random.randn(32, nparams)
    nwalkers, ndim = pos.shape

    sampler = emcee.EnsembleSampler(nwalkers, ndim, post, args=args)
    sampler.run_mcmc(pos, 5000, progress=True)

    
    # JAB Plot steps and parameters
    if steps:
        fig, axes = plt.subplots(2, figsize=(10, 7), sharex=True)
        samples = sampler.get_chain()
        for i in range(ndim):
            ax = axes[i]
            ax.plot(samples[:, :, i], "k", alpha=0.3)
            ax.set_xlim(0, len(samples))
            ax.set_ylabel(labels[i])
            ax.yaxis.set_label_coords(-0.1, 0.5)

        axes[-1].set_xlabel("step number");
        plt.show()

    # JAB Make corner plot of results with true values if entered
    flat_samples = sampler.get_chain(discard=100, thin=15, flat=True)

    fig = corner.corner(flat_samples, labels=labels, truths=truths);
    plt.show()

    # JAB Determine the best values of the parameters
    fits = []
    for i in range(ndim):
        mcmc = np.percentile(flat_samples[:, i], [16, 50, 84])
        q = np.diff(mcmc)
        fits.append([labels[i], mcmc[1], q[0], q[1]])

    return fits

if __name__ == '__main__':
    # JAB Read in data file
    filepath = '/d/scratch/ASTR5160/final/dataxy.fits'
    data = Table.read(filepath)

    x, y, yerr = data['x'], data['y'], data['yerr']

    # JAB Use emcee to find linear fit
    nparams = 2
    m_start = -1
    b_start = 5
    mrange = [-2,1]
    brange = [-5,10]
    args = (x, y, (yerr**2), mrange, brange)
    labels = ['m', 'b']

    fits = use_emcee([m_start, b_start], log_posterior, args, labels, steps=True)
    print(fits[0])
    print(fits[1])
