#Jasmine Garani
#9/19/17

import numpy
from astropy.time import Time
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import AltAz
from astropy.coordinates import EarthLocation


coords = SkyCoord(ra=300.17917*u.degree, dec=22.71083*u.degree, frame='icrs')

observing_location = EarthLocation(lat=40.914224*u.deg, lon=-73.11623*u.deg, height=0)
times = Time(2458026.541667,format='jd')


aa = AltAz(location=observing_location, obstime=times)
aacoords = coords.transform_to(aa)
print aacoords.az #209d06m24.5343s
print aacoords.alt #69d49m13.2803s

#commented numbers are what I got for those values - Jasmine
