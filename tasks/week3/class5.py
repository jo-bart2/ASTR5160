import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord, EarthLocation
import astropy.units as u
from astropy.time import Time

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

#JAB create function to convert from equatorial to cartesian with equations
def convert(Ra,Dec):
    coor = SkyCoord(Ra,Dec,frame='icrs')
    new_x = np.cos(coor.ra.radian)*np.cos(coor.dec.radian)
    new_y = np.sin(coor.ra.radian)*np.cos(coor.dec.radian)
    new_z = np.sin(coor.dec.radian)
    
    return new_x,new_y,new_z

#JAB create function to check whether SkyCoord conversion and equations match
def match(Ra,Dec,x,y,z):
    x = float(x)
    y = float(y)
    z = float(z)
    
    x2,y2,z2 = convert(Ra,Dec)
    
    if round(x2,10) == round(x,10) and round(y2,10) == round(y,10) and round(z2,10) == round(z,10):
        print('SkyCoord output matches given equations')

    else:
        print('SkyCoord output does not match given equations')

#JAB run functions        
match(r,d,coords.x,coords.y,coords.z)

#JAB calculate the ra and dec of the galactic center: (0,0) in (l,b)
l = 0
b = 0

center = SkyCoord(l*u.degree,b*u.degree,frame='galactic')
equ = center.icrs
print('The coordinates of the galactic center are: '+equ.to_string('hmsdms'))
#These coordinates are in the constellation Sagittarius.
#It is near the edge of the constellation

#JAB Plot change in galactic coordinates over a year at zenith
z = 40

#JAB function to convert from equatorial to galactic
def EquToGal(alpha,delta):
    coord = SkyCoord(alpha,delta,frame='icrs',unit='deg')
    gal = coord.galactic
    
    return gal

#JAB Location of Laramie
lati = 40
long = 105+(59/60)+(11/3600)
h = 2184
laramie = EarthLocation(lat=lati,lon=long,height=h)

#JAB function to find local sidereal time from location and time
def FindRA(loc,time):
    sid = []
    for i in time:
        t = Time(i, scale='utc', location=loc)
        sid.append(t.sidereal_time('mean'))
    return sid

#JAB function to create list of dates and times for a year
def makeTime():
    date = Time(Time.now())
    times = []
    for i in range(366):
        times.append(date+i*u.day)
    return times

#JAB put it all together to get lists of l and b for a year
def allTogether(dec,sids,loc):
    times = makeTime()
    lst = FindRA(loc,times)
    
    ls = []
    bs = []
    
    for x in lst:
        gals = EquToGal(x,dec)
        ls.append(gals.l.degree)
        bs.append(gals.b.degree)
    
    return ls,bs

times = makeTime()
l_list,b_list = allTogether(z,times,laramie)

plt.scatter(l_list,b_list,color='black')
plt.xlabel('Galactic Longitude l (deg)')
plt.ylabel('Galactic Latitude b (deg)')
plt.show()

    
    
    
    




