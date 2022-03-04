import numpy as np
import matplotlib.pyplot as plt

def field_area(r_min, r_max, d_min, d_max):
    '''
    Parameters
    ----------
    r_min: :class: 'integer' or 'float'
         The minimum RA of the rectangle in degrees
    
    r_max: :class: 'integer' or 'float'
         The maximum RA of the rectangle in degrees
    
    d_min: :class: 'integer' or 'float
         The minimum Dec of the rectangle in degrees
    
    d_max: :class: 'integer' or 'float
         The maximum Dec of the rectangle in degrees

    Returns
    -------
    area: :class: 'integer' or 'float'
    '''
    
    # JAB Determine the area of the lat-lon rectangle
    z1, z2 = np.sin(np.deg2rad(d_min)), np.sin(np.deg2rad(d_max))
    area = (r_max-r_min)*(z2-z1)

    return area


def populate():
    '''
    Parameters
    ----------
    Returns
    -------
    '''

def plot_rect(coords):
    '''
    Parameters:
    -----------
    Returns:
    --------
    '''
    
    # JAB Determine the number of rectangles to plot
    num = 

if __name__ == '__main__':
    
    # JAB Check function returns the correct value for (0,360,0.90)
    a = field_area(0,360,0,90)
    print('The area of a rectangle bounded by (0, 360, 0, 90) is: {}'.format(a))
