#Jasmine Garani, Lorena Mezini, Patrick Payne
#Start date 9/13/17

import numpy as np
from astropy.io import fits
import os
import warnings
from astropy.utils.exceptions import AstropyWarning
warnings.simplefilter('ignore',category=AstropyWarning)
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm


#==========================================================================

jasminepath = "/Users/Jasmine/Documents/stony_brook/y4_sb/ast443/CGS-Groupdata/lab0/BigCCD/bigCCD-data/"
lorenapath = "/home/icecube/AST/CGS-GroupData/AST443/CGS-GroupData/lab0/BigCCD/bigCCD-data/"
patrickpath = "/Users/ilovealltigers/SBU_F17/AST_443/LAB1/CGS-GroupData/lab0/BigCCD/bigCCD-data/"

def badpixmapping(path):
    all_flats = []
#    hdulist1 = fits.open(path + '/' + 'flat-expos23s-Neg5-Vis.00000009.FIT', ignore_missing_end=True)
    for f in os.listdir(path):
        if "flat" in f and "FIT" in f:
            print f
            hdulist = fits.open(jasminepath + '/' + f,ignore_missing_end=True)
            header = hdulist[0].header
            imagedata = hdulist[0].data
            norm_data = imagedata/np.median(imagedata)
            all_flats.append(norm_data)

    
    master_flat = np.median(all_flats,axis=0)
    master_flat = master_flat/np.mean(master_flat)

            
    std = np.std(master_flat)
    mean = np.mean(master_flat)
    print 'standard deviation = ', std
    print mean - 5.*std

    badpix=np.zeros((1024,1024))
    print badpix.shape, type(badpix)

    for i in range(0,len(master_flat[0])):
        for k in range(0,len(master_flat[1])):
            if master_flat[i][k] <= mean - 5.*std:
                badpix[i][k]=0
            else:
                badpix[i][k]=1
        
    ###########################################################
    
    filename = 'darks-expos300s-Neg10-Vis.00000000.DARK.FIT'
    hdulist2 = fits.open(path + '/' + filename)
    imagedata2 = hdulist2[0].data
    countvalues = imagedata2.flatten()
    cmin2 = 950
    cmax2 = 1150
    nbins2 = 100

    normalization = ((cmax2-cmin2)/nbins2)*len(countvalues[(countvalues>=cmin2) & (countvalues<=cmax2)])
    meandark = np.mean(countvalues) #mean of single image
    sigdark = np.std(countvalues[countvalues<=cmax2]) #standard deviation of single image
    

    for i in range(0,len(master_flat[0])):
        for k in range(0,len(master_flat[1])):
            if master_flat[i][k] >= meandark + 5.*sigdark or badpix[i][k] == 0:
                badpix[i][k]=0
            else:
                badpix[i][k]=1

    badpixmap = fits.PrimaryHDU(badpix)
    badpixmap.writeto('badpixmap.fits',clobber=True)

badpixmapping(path)                

#THE END, i'll try harder next time :(

#==============================================================================
