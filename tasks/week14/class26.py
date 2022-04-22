import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
import emcee
import corner
from tasks.week13.class23 import linear

# JAB Separate function for the log prior
def log_prior(mb, mminmax, bminmax):
    '''
    Parameters
    ----------
    mb: :class: 'list', '~numpy.ndarray'
       An array or list of the two values for m and b in the shape [m, b]

    mminmax: :class: 'list', '~numpy.ndarray'
       An array or list of the two values determining the prior range of m
       in the shape of [m_min, m_max]

    bminmax: :class: 'list', '~numpy.ndarray'
       An array or list of the two values determining the prior range of b
       in the shape of [b_min, b_max]

    Returns
    -------
    lnprior: :class: 'float'
       The value of the natural log of the prior
    '''
    m, b = mb
    m_min, m_max = mminmax
    b_min, b_max = bminmax

    if m_min <= m <= m_max and b_min <= b <= b_max:
        lnprior = 0.0
    else:
        lnprior = -np.inf

    return lnprior


# JAB Rewrite posterior probability function
def log_posterior(mb, xs, ys, var, mminmax, bminmax):
    '''
    Parameters
    ----------
    mb: :class: 'list', '~numpy.ndarray'
       An array or list of the two values for m and b in the shape [m, b]

    xs: :class: '~numpy.ndarray'
       An array of the x values of the data
    
    ys: :class: '~numpy.ndarray'
       An array of the y values of the data

    var: :class: '~numpy.ndarray'
       An array of the variances of the data
    
    mminmax: :class: 'list', '~numpy.ndarray'
       An array or list of the two values determining the prior range of m
       in the shape of [m_min, m_max]

    bminmax: :class: 'list', '~numpy.ndarray'
       An array or list of the two values determining the prior range of b
       in the shape of [b_min, b_max]

    Returns
    -------
    lnpost: :class: 'float'
       The natural log the of the posterior probability

    '''
    m, b = mb
    lnprior = log_prior(mb, mminmax, bminmax)

    # JAB Calculate the predicted y values for the model
    ymodel = linear(m, xs, b)

    # JAB Calculate the natural log of the likelihood
    lnlike = (-0.5)*sum(((ys - ymodel)**2)/var + np.log(2*np.pi*var))

    # JAB Calculate the natural log of the posterior probability
    lnpost = lnprior + lnlike

    return lnpost
    
if __name__ == '__main__':
    # JAB Problem 1
    # JAB Read in file and find mean and variance of each bin
    filepath = '/d/scratch/ASTR5160/week13/line.data'
    data = Table.read(filepath, format='ascii')
    
    x = np.linspace(0.5, 9.5, 10)
    mean = np.array([np.mean(data['col{}'.format(i)]) for i in range(1,11)])
    var = np.array([np.var(data['col{}'.format(i)], ddof=1) for i in range(1,11)])

    # JAB Problem 2
    # JAB Use example tutorial of emcee to find best fit
    nparams = 2
    m_start = 3
    b_start = 5

    pos = np.array([m_start, b_start]) + 1e-4 * np.random.randn(32, nparams)
    nwalkers, ndim = pos.shape

    sampler = emcee.EnsembleSampler(nwalkers, ndim, log_posterior, args=(x, mean, var, 
                                                                         [2,4], [4,6]))

    sampler.run_mcmc(pos, 5000, progress=True)

    # JAB Plot steps and parameters
    fig, axes = plt.subplots(2, figsize=(10, 7), sharex=True)
    samples = sampler.get_chain()
    labels = ["m", "b"]
    for i in range(ndim):
        ax = axes[i]
        ax.plot(samples[:, :, i], "k", alpha=0.3)
        ax.set_xlim(0, len(samples))
        ax.set_ylabel(labels[i])
        ax.yaxis.set_label_coords(-0.1, 0.5)

    axes[-1].set_xlabel("step number");
    plt.show()

    # JAB Make corner plot of results with true values as m=3 and b=4.8
    flat_samples = sampler.get_chain(discard=100, thin=15, flat=True)

    fig = corner.corner(flat_samples, labels=labels, truths=[3.0, 4.8]);
    plt.show()

    # JAB Plot some of results over the data
    inds = np.random.randint(len(flat_samples), size=100)
    for ind in inds:
        sample = flat_samples[ind]
        plt.plot(x, np.dot(np.vander(x, 2), sample[:2]), "C1", alpha=0.1)
    plt.scatter(x, mean, color="k")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

    # JAB Determine the best values of m and b
    for i in range(ndim):
        mcmc = np.percentile(flat_samples[:, i], [16, 50, 84])
        q = np.diff(mcmc)
        print(labels[i], mcmc[1], q[0], q[1])
