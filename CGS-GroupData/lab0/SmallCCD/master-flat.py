#Jasmine Garani, Patrick Payne, Lorena Mezini
#Start date 9/20/17
#Code for making master flats for spectroscopy

import numpy as np
from astropy.io import fits
import os
#===================================================================
jasminepath = '/Users/Jasmine/Documents/stony_brook/y4_sb/ast443/CGS-Groupdata/lab0/SmallCCD/smallCCD-data/'

path = jasminepath #change this to your path

def masterflat(path):
    all_flats = []
    for f in os.listdir(path):
        if "flat" in f:
            print f
            hduflats = fits.open(path + '/' + f,ignore_missing_end=True)
            header = hduflats[0].header
            imagedata = hduflats[0].data
            all_flats.append(imagedata)
    master_flat = np.median(all_flats,axis=0)
    outflathdu = fits.PrimaryHDU(master_flat)
    outflathdu.writeto(path + '/' + 'spec-master-flat.fits',clobber=True)


masterflat(path)
