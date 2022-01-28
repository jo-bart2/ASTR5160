import numpy as np
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
import astropy.units as u

#JAB RA and Dec of the star Procyon
r = '07h39m18s' #RA
d = '+05d13m30s' #Dec

#JAB Convert RA and Dec to degrees with astropy
deg = SkyCoord(r,d,frame='icrs')
print('The RA and Dec of Procyon in degrees is ' + str(deg.ra.degree) + ', ' + str(deg.dec.degree))

#JAB Confirm they match given equations
def match(ra, dec):
    
    deg = SkyCoord(ra,dec,frame='icrs')
    
    delim = 'hmsd'
    for i in delim:
        ra = ra.replace(i,',')
        dec = dec.replace(i,',')

    rlist = ra.split(',')
    dlist = dec.split(',')
    
    rdeg = 15*(int(rlist[0]) + int(rlist[1])/60 + int(rlist[2])/3600)
    ddeg = int(dlist[0]) + int(dlist[1])/60 + int(dlist[2])/3600
    
    if round(rdeg,3) == round(deg.ra.degree,3) and round(ddeg,3) == round(deg.dec.degree,3):
        print('RA and Dec Calculations Correct:')
        print(str(rdeg)+' = '+str(deg.ra.degree)+', '+str(ddeg)+' = '+str(deg.dec.degree))
    else:
        print('RA and Dec Calculations Incorrect:')
        print(str(rdeg)+' does not equal '+str(deg.ra.degree)+', '+str(ddeg)+' does not equal '+str(deg.dec.degree))

#JAB Run match function to confirm that astropy function is the same as given equations
match(r,d)

#JAB Determine current JD and MJD
date = Time(Time.now())
mjd = date.mjd
jd = date.jd

#JAB Confirm JD and MJD are accurate to given equations
if round(mjd,8) == round(jd-2400000.5,8):
    print('Calculations correct: MJD = JD - 2400000.5')
else:
    print('Calculations incorrect: MJD != JD - 2400000.5')

#JAB List days near today's MJD
days = np.arange(mjd-10,mjd+10)
print('The following list is MJDs from the current MJD-10 to MJD+10:')
print(days)

#JAB Set location of WIRO from 41 5'49"N, 105 58'33"W, 2943m
lati = 41+(5/60)+(49/3600)
long = 105+(58/60)+(33/3600)
h = 2943
wiro = EarthLocation(lat=lati,lon=long,height=h)

#JAB Find airmass towards star at 12h, 30N
coord = SkyCoord('12h','30d', frame='icrs')
utcoffset = -7*u.hour #utc offset from MST

#JAB Find airmass at 11pm tonight
now11 = Time('2022-1-28 23:00:00') - utcoffset #Find date and time of observation
staraltaz_now = coord.transform_to(AltAz(obstime=now11,location=wiro)) #find alt az of star
starairmass_now = staraltaz_now.secz #convert alt az to airmass
print('The airmass of the star is '+str(starairmass_now)+' at 11pm today')
#JAB Find airmass at 11pm next month
next11 = Time('2022-2-28 23:00:00') - utcoffset #Find date and time of observation
staraltaz_next = coord.transform_to(AltAz(obstime=next11,location=wiro)) #find alt az of star
starairmass_next = staraltaz_next.secz #convert alt az to airmass
print('The airmass of the star is '+str(starairmass_next)+' at 11pm 1 month from now')


