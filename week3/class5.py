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
    new_x = np.cos(coor.ra.radian)*np.cos(coor.dec.radian)
    new_y = np.sin(coor.ra.radian)*np.cos(coor.dec.radian)
    new_z = np.sin(coor.dec.radian)
    
    return new_x,new_y,new_z

def match(Ra,Dec,x,y,z):
    x = float(x)
    y = float(y)
    z = float(z)
    
    x2,y2,z2 = convert(Ra,Dec)
    
    #if x2 == x and y2 == y and z2 == z:
    if round(x2,10) == round(x,10) and round(y2,10) == round(y,10) and round(z2,10) == round(z,10):
        print('SkyCoord output matches given equations')
        print(x,y,z)
        print(x2,y2,z2 )
    else:
        print('SkyCoord output does not match given equations')
        print(x,y,z)
        print(x2,y2,z2 )
        
match(r,d,coords.x,coords.y,coords.z)