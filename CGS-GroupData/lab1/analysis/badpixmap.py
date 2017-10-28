#Jasmine Garani, Lorena Mezini, Patrick Payne
#Start Date 10/5/17
#Purpose: this code creates the bad pixel map for the master flat

import numpy as np
from astropy.io import fits


#======================================================

jasminepath = '/home/jgarani/AST443/CGS-GroupData/lab1/analysis/'

path = jasminepath

def badpixmap(path):
    #get the master flat
    hduflat = fits.open(path + '/' + 'master_flat.fits')
    master_flat = hduflat[0].data
    masterflatten = master_flat.flatten() #flattened flat data
    
    #Calculate the standard deviation and the mean
    std = np.std(masterflatten)
    mean = np.mean(masterflatten)

    #Initialize bad pixel array
    badpix = np.zeros((1024,1024))
    
    #Calculates and assigns value to 0 to dead pixels, and 1 to undead pix
    for i in range(0,len(master_flat[0])):
        for k in range(0,len(master_flat[1])):
            if master_flat[i][k] <= mean - 5.*std:
                badpix[i][k] = 0
            else:
                badpix[i][k]=1
    
    #get the master dark
    hdudark = fits.open(path + '/' + 'master_dark.fits')
    master_dark = hdudark[0].data
    masterdarken = master_dark.flatten() #flattened dark data
    
    #caluclate mean and standard deviation
    meandark = np.mean(masterdarken)
    sigdark = np.std(masterdarken)
    
    #Calculates and assigns value of 0 to the hot pixels, and preserves the dead pixels
    for j in range(0,len(master_dark[0])):
        for g in range(0,len(master_dark[1])):
            if master_dark[j][g] >= meandark + 5.*sigdark or badpix[j][g] == 0:
                badpix[j][g] = 0
            else:
                badpix[j][g] = 1
    badpixmap = fits.PrimaryHDU(badpix)
    badpixmap.writeto(path + '/' + 'badpixmap.fits',overwrite=True)


badpixmap(path)
