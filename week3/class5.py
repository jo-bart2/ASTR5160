import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord

#JAB RA and Dec of the star Procyon
r = '07h39m18s' #RA
d = '+05d13m30s' #Dec

#JAB Convert RA and Dec to cartesian with astropy
coords = SkyCoord(r,d,frame='icrs')
coords.representation_type = 'cartesian'
print('The coordinates of Procyon in cartesian are:')
print('x = ' + str(coords.x))
print('y = ' + str(coords.y))
print('z = ' + str(coords.z))

#JAB Check SkyCoord matches given equations
def convert(Ra,Dec):
    coor = SkyCoord(Ra,Dec,frame='icrs')
    print(coor.dec.degree)
    new_x = float(np.cos(coor.ra.degree)*np.cos(coor.dec.degree))
    new_y = float(np.sin(coor.ra.degree)*np.cos(coor.dec.degree))
    new_z = float(np.sin(coor.dec.degree))
    
    return new_x,new_y,new_z

def match(Ra,Dec,x,y,z):
    x = float(x)
    y = float(y)
    z = float(z)
    
    x2,y2,z2 = convert(Ra,Dec)
    
    if round(x2,4) == round(x,4) and round(y2,4) == round(y,4) and round(z2,4) == round(z,4):
        print('SkyCoord output matches given equations')
        print(x,y,z)
        print(x2,y2,z2 )
    else:
        print('SkyCoord output does not match given equations')
        print(x,y,z)
        print(x2,y2,z2 )
        
match(r,d,coords.x,coords.y,coords.z)