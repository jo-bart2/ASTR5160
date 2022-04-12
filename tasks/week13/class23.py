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

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(x, means, color='k', label='Data')

for i in range(len(mguess)):
    ax.plot(x, linear(mguess[i], x, bguess[i]), color=colors[i], label=
            'y = {}x + {}'.format(mguess[i], bguess[i]), linestyle='dashed')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.legend()
plt.show()


