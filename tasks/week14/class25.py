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

def mcmc_walk(m_start, x, b_start, ys, var, m_min, m_max, b_min, b_max, num, step):
    '''
    Parameters
    ----------
    m_start: :class: 'int', 'float'
       The starting value of the slope

    x: :class: '~numpy.ndarray'
       An array of x values for the data

    b_start: :class: 'int', 'float'
       The starting value of the y intercept

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

    num: :class: 'int'
       The number of steps to take in the MCMC

    step: :class: 'int', 'float'
       The value of the step size for the walk
    
    Returns
    -------
    ms: :class: '~numpy.ndarray'
       An array of the accepted slope values

    bs: :class: '~numpy.ndarray'
       An array of the accepted y-intercept values

    posts: :class: '~numpy.ndarray'
       An array of the posterior probabilities of the accepted m and b values

    '''
    # JAB Step through m and b 
    ms = np.array([m_start])
    bs = np.array([b_start])
    posts = np.array([posterior(m_start, x, b_start, ys, var, m_min, m_max, b_min, b_max)])
    i = 1

    for steps in range(1,num):
        # JAB Find new and old m and b
        m_old = ms[i-1]
        m_new = m_old + np.random.normal(0, step)

        b_old = bs[i-1]
        b_new = b_old + np.random.normal(0, step)

        # JAB Calculate posterior probabilities
        p_old = posts[i-1]
        p_new = posterior(m_new, x, b_new, ys, var, m_min, m_max, b_min, b_max)
        
        # JAB Find R value
        R = p_new/p_old
        
        # JAB Accept or reject parameters
        rand = np.random.random(1)
        if R > 1 or rand < R < 1:
            ms = np.append(ms, m_new)
            bs = np.append(bs, b_new)
            posts = np.append(posts, p_new)
            
            i += 1
    
    return ms, bs, posts
    

if __name__ == '__main__':
    # JAB Problem 1
    # JAB Read in file and find mean and variance of each bin
    filepath = '/d/scratch/ASTR5160/week13/line.data'
    data = Table.read(filepath, format='ascii')
    
    x = np.linspace(0.5, 9.5, 10)
    mean = np.array([np.mean(data['col{}'.format(i)]) for i in range(1,11)])
    var = np.array([np.var(data['col{}'.format(i)], ddof=1) for i in range(1,11)])

    # JAB Problem 3
    steps = 1000
    m_acc, b_acc, post_acc = mcmc_walk(3, x, 5, mean, var, 2, 4, 4, 6, steps, 0.05)
    print('Best fit: m = {}, b = {}'.format(m_acc[post_acc == max(post_acc)][0], 
                                            b_acc[post_acc == max(post_acc)][0]))

    # JAB Problem 4
    print('The acceptance rate is {}%'.format(len(m_acc)/steps*100))
    # JAB The accpetance rate varies quite a bit, but by changing the step size 
    # to 0.05 from 0.1, it is generally near 30%
