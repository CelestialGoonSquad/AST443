#This is used to put things in the header of files


import numpy as np
from astropy.io import fits


science,hdr = fits.getdata('/home/jgarani/AST443/CGS-GroupData/lab2/forpyraf/hg/' + 'all-images.CF.ms.L.fits', header=True)

hdr['exptime'] = 240.
hdr['airmass'] = 1.

fits.writeto('/home/jgarani/AST443/CGS-GroupData/lab2/forpyraf/hg/' + 'all\
-images.CF.ms.L.fits', science, header=hdr,overwrite=True)
