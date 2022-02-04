import numpy as np
import matplotlib.pyplot as plt

#JAB Problem 1
def linear(m,b):
    """

    Parameters
    ----------
    m : :class: 'float' or 'integer'
        The slope of the line to be created
    b : :class: 'float' or 'integer'
        The y-intercept of the line to be created

    Returns
    -------
    x : :class: '~numpy.ndarray'
        The randomly generated x values
    offset : :class: '~numpy.ndarray'
        The corresponding y values offset from a Gaussian distribution
    y_err : :class: '~numpy.ndarray'
        The error on y. Always 0.5

    """
    #JAB (i) Generate 10 floating point numbers at random for x axis
    x = np.random.uniform(0,10,10)
    
    #JAB (ii) Recover appropriate linear y values
    y = x*m+b
        
    #JAB (iii) Scatters y values
    offset = [np.random.normal(i,scale=0.5) for i in y]
    y_err = np.linspace(0.5,0.5,10)
    
    return x, offset, y_err

linear(1,2)
