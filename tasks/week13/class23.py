import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2
from astropy.table import Table

def linear(m, x, b):
    '''
    Parameters
    ----------
    m: :class: 'int', 'float'
       The slope of the line

    x: :class: 'int', 'float', '~numpy.ndarray'
       Either a single x valur or an array of x values

    b: :class: 'int', 'float'
       The y-intercept of the line

    Returns
    -------
    y: :class: 'int', 'float', '~numpy.ndarray'
       The output of the linear function y = mx + b
    '''
    y = m*x + b
    
    return y
if __name__ == '__main__':
    # JAB Problem 1
    # JAB Read in file
    filepath = '/d/scratch/ASTR5160/week13/line.data'
    data = Table.read(filepath, format='ascii')
    
    # JAB Find mean and variance of each x bin
    x = np.linspace(0.5, 9.5, 10)
    means = np.array([np.mean(data['col{}'.format(i)]) for i in range(1,11)])
    varis = np.array([np.var(data['col{}'.format(i)], ddof=1) for i in range(1,11)])

    # JAB Problem 2
    # JAB Plot data and model lines
    mguess = np.array([2.5, 2.5, 2.5, 3, 3, 3, 3.5, 3.5, 3.5]) 
    bguess = np.array([4, 4.5, 5, 4, 4.5, 5, 4, 4.5, 5])
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'orange', 'purple', 'pink']
    
    ymodel = np.array([linear(mguess[i], x, bguess[i]) for i in range(len(mguess))])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x, means, color='k', label='Data')

    for i in range(len(mguess)):
        ax.plot(x, ymodel[i], color=colors[i], label='y = {}x + {}'.format(
            mguess[i], bguess[i]), linestyle='dashed')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    plt.show()

    # JAB Problem 3
    # JAB Determine the Chi squared for each m and b fit
    chi = np.array([sum((means - i)**2 / varis**2) for i in ymodel])

    # JAB Problem 4
    # JAB Plot m and b against chi squared
    labels = ['{},{}'.format(mguess[i], bguess[i]) for i in range(len(mguess))]
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.bar(range(0,9), chi, tick_label=labels)
    ax2.set_xlabel('m, b')
    ax2.set_ylabel('Chi Squared')
    plt.show()

    # JAB Print out best fit parameters
    chimin = min(chi)
    b_best = bguess[chi == chimin]
    m_best = mguess[chi == chimin]

    print('The minimum Chi squared is: {}'.format(chimin))
    print('The best fit parameters are: m = {} and b = {}'.format(m_best[0], b_best[0]))

    # JAB Problem 5
    # JAB Calculate delta chi squared for each model
    delta_chi = chi - chimin

    # JAB Determine the 68% and 95% confidence limits
    sig1 = 0.32
    sig2 = 0.05
    df = len(x) - 2 - 1

    probs = chi2.sf(delta_chi, df)
    cl68 = delta_chi[probs > sig1]
    cl95 = delta_chi[probs > sig2]

    print(len(cl68),len(cl95))





