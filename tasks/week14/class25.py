import numpy as np
from astropy.table import Table
from tasks.week13.class23 import linear

# JAB Function to calculate posterior probability
def posterior(m, x, b, ys, var, m_min, m_max, b_min, b_max):
    '''
    Parameters
    ----------
    m: :class: 'int', 'float'
       The slope of the model line

    x: :class: '~numpy.ndarray'
       An array of x values for the data

    b: :class: 'int', 'float'
       The y-intercept of the model line

    ys: :class: '~numpy.ndarray'
       An array of the y data points 

    var: :class: '~numpy.ndarray'
       The variances of the data

    m_min: :class: 'int', 'float'
       The minimum value for the Prior of the slope

    m_max: :class: 'int', 'float'
       The maximum value for the Prior of the slope

    b_min: :class: 'int', 'float'
       The minimum value for the Prior of the intercept

    b_max: :class: 'int', 'float'
       The maximum value for the Prior of the intercept

    Returns
    -------
    prob: :class: 'float'
       The natural log of the posterior probability

    '''
    # JAB Calculate the predicted y values for the model
    ymodel = linear(m, x, b)

    # JAB Find the posterior probability
    prob = (-0.5)*sum(((ys - ymodel)**2)/var + np.log(2*np.pi*var))

    # JAB Check the m and b prior conditions
    if b < b_min or b > b_max or m < m_min or m > m_max:
        prob = -np.inf

    return prob

def mcmc_walk():
    '''
    Parameters
    ----------
    Returns
    -------
    '''
    # JAB Step through m and b 
    for i in range(num):
        
    

if __name__ == '__main__':
    # JAB Problem 1
    # JAB Read in file and find mean and variance of each bin
    filepath = '/d/scratch/ASTR5160/week13/line.data'
    data = Table.read(filepath, format='ascii')
    
    x = np.linspace(0.5, 9.5, 10)
    mean = np.array([np.mean(data['col{}'.format(i)]) for i in range(1,11)])
    var = np.array([np.var(data['col{}'.format(i)], ddof=1) for i in range(1,11)])

    # JAB Problem 3
    
