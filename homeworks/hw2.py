import numpy as np
import matplotlib.pyplot as plt
import argparse

def field_area(r_min, r_max, d_min, d_max):
    '''
    Parameters
    ----------
    r_min: :class: 'integer' or 'float'
         The minimum RA of the rectangle in degrees from 0 to 360
    
    r_max: :class: 'integer' or 'float'
         The maximum RA of the rectangle in degrees from 0 to 360
    
    d_min: :class: 'integer' or 'float
         The minimum Dec of the rectangle in degrees from -90 to 90
    
    d_max: :class: 'integer' or 'float
         The maximum Dec of the rectangle in degrees from -90 to 90

    Returns
    -------
    area: :class: 'integer' or 'float'
    '''
    
    # JAB Determine the area of the lat-lon rectangle
    z1, z2 = np.sin(np.deg2rad(d_min)), np.sin(np.deg2rad(d_max))
    area = (r_max-r_min)*(z2-z1)*(180/np.pi)

    return area

def plot_rect(coords, plot_dir):
    '''
    Parameters:
    -----------
    coords: :class: '~numpy.ndarray'
          An array of arrays containing ra and dec boundaries of each rectangle
          in the form [ra_min. ra_max, dec_min, dec_max] where ra is from -180 to 180
          and dec is from -90 to 90

    dir: :class: 'string'
       The string representing the directory in which to save the plot
    '''

    # JAB Determine the area of each rectangle
    area = [field_area(i[0], i[1], i[2], i[3]) for i in coords]
    
    # JAB Convert ra and dec to radians
    c_rad = [[np.deg2rad(i[0]), np.deg2rad(i[1]), np.deg2rad(i[2]), 
              np.deg2rad(i[3])] for i in coords]
    
    # JAB Determine lines to be plotted
    l_r_min = [[np.linspace(i[0], i[0]), np.linspace(i[2], i[3])] for i in c_rad]
    l_r_max = [[np.linspace(i[1], i[1]), np.linspace(i[2], i[3])] for i in c_rad]
    l_d_min = [[np.linspace(i[0], i[1]), np.linspace(i[2], i[2])] for i in c_rad]
    l_d_max = [[np.linspace(i[0], i[1]), np.linspace(i[3], i[3])] for i in c_rad]
    # JAB Make list of colors for plots
    clrs = ['r','g','c','m', 'y', 'purple', 'orange']
    # JAB Plot the rectangles on the sphere
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='aitoff')
    for i in range(len(l_r_min)):
        ax.plot(l_r_min[i][0], l_r_min[i][1], color=clrs[i])
        ax.plot(l_r_max[i][0], l_r_max[i][1], color=clrs[i])
        ax.plot(l_d_min[i][0], l_d_min[i][1], color=clrs[i])
        ax.plot(l_d_max[i][0], l_d_max[i][1], color=clrs[i])
        ax.fill_between(l_d_min[i][0], l_d_min[i][1], l_d_max[i][1], color=clrs[i], 
                        label='Area = {} sqr deg'.format(round(area[i],2)), alpha=0.5)
    ax.grid(color='k', linestyle='solid', linewidth=0.6)
    ax.legend()
    plt.savefig('{}/plot1.png'.format(plot_dir))
    plt.show()


def populate(r_min, r_max, d_min, d_max):
    '''
    Parameters
    ----------
    r_min: :class: 'integer' or 'float'
         The minimum RA of the rectangle in degrees from 0 to 360
    
    r_max: :class: 'integer' or 'float'
         The maximum RA of the rectangle in degrees from 0 to 360
    
    d_min: :class: 'integer' or 'float
         The minimum Dec of the rectangle in degrees from -90 to 90
    
    d_max: :class: 'integer' or 'float
         The maximum Dec of the rectangle in degrees from -90 to 90

    Returns
    -------
    ra_in: :class: '~numpy.ndarray'
         An array of RAs for the points on the sphere inside the rectangle

    dec_in: :class: '~numpy.ndarray'
          An array of Decs for the points on the sphere inside the rectangle
    '''
    
    # JAB Populate entire sphere randomly in area
    ra = 360.*(np.random.random(100000))
    dec = (180/np.pi)*np.arcsin(1.-np.random.random(100000)*2.)
    
    # JAB Determine ra and dec points within rectangle
    ra_in = [ra[i] for i in range(len(ra)) if r_min < ra[i] < r_max and d_min < dec[i] < d_max]
    dec_in = [dec[i] for i in range(len(ra)) if r_min < ra[i] < r_max and d_min < dec[i] < d_max]

    return ra_in, dec_in

if __name__ == '__main__':
    # JAB Part 1
    # JAB Get input for directory to save figure to
    parser = argparse.ArgumentParser(
        'Make figures and save them to a particular directory')
    parser.add_argument('directory', help='The directory to save plots to')
    args = parser.parse_args()
    plot_dir = args.directory

    # JAB Check function returns the correct value for (0, 360, 0, 90)
    a = field_area(0, 360, 0, 90)
    print('The area of a rectangle bounded by (0, 360, 0, 90) is: {} square degrees'
          .format(a))

    # JAB Create list of rectangle coordinates and plot
    ra_min = np.array([np.random.randint(-180,167)]*4)
    ra_max = ra_min+45
    dmin = np.random.randint(-90, -70)
    dec_min = [dmin+i*45 for i in range(4)]
    dec_max = [i+20 for i in dec_min]

    c = [[ra_min[i], ra_max[i], dec_min[i], dec_max[i]] for i in range(len(ra_min))]

    plot_rect(c, plot_dir)

    # JAB Part 2
    # JAB Randomly populate sphere
    ra, dec = populate(ra_min[2]+180, ra_max[2]+180, dec_min[2], dec_max[2])
    
    # JAB Determine the expected number of points in rectangle
    area_rec = field_area(ra_min[2]+180, ra_max[2]+180, dec_min[2], dec_max[2])
    area_full = field_area(0, 360, -90, 90)
    f = area_rec/area_full
    num_ex = f*100000 
    
  
    # JAB Determine if these two values match
    if len(ra)-300 < round(num_ex,0) < len(ra)+300:
        print('The lat-lon rectangle contains roughly the correct number of points:')
        print('{} is close to {}'.format(round(num_ex,0), len(ra)))
    else:
        print('The lat-lon rectangle does not contain roughly the correct number of points')
        
    
