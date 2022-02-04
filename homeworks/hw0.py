import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#JAB Problem 1: Create function to return x,y, and y_err
def CreateArrays(m,b):
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

#JAB Problem 2: Fit a straight line and recover values of m2 and b2
x, y, y_err = CreateArrays(2,1) #Given values of m=2, b=1

def linear(x2,m2,b2):
    return m2*x2 + b2

popt, pcov = curve_fit(linear,x,y,sigma=y_err)
print('The recovered values are: m = '+str(popt[0])+', b = '+str(popt[1]))





