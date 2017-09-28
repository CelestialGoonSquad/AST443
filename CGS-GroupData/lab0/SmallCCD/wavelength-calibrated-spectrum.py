#Jasmine, Lorena, Patrick
#9/27/17
#Code for extracting data from wavelength calibrated spectrum and plotting using python


import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
#===============================================
jasminepath = "/home/jgarani/AST443/CGS-GroupData/lab0/SmallCCD/smallCCD-data/"

path = jasminepath

def spectrum(path):
    speclist = fits.open(path + '/' + "spec-norm-Neg5-tel-expo30s-3x3.00000003.ms.L.fits")
    imagedata = speclist[0].data #this is the y-array, counts
    header = speclist[0].header
    print imagedata.shape
    print type(imagedata)
    print imagedata 
    print np.where(imagedata == imagedata[10])
    val1 = header['CRVAL1']
    delta = header['CDELT1']
    values = np.zeros(255) #this is the x-array, wavelength values
    for i in range(0,len(imagedata)):
        values[i] = val1 + i*delta
    print values
    print values.shape
    print type(values)
    
    plt.plot(values,imagedata)
    plt.xlabel(r'Wavelength (\AA)'
    plt.ylabel(r'Counts')
    #plt.savefig(path + '/' + "spectrum.png",format='png')
    #plt.show()


spectrum(path)
