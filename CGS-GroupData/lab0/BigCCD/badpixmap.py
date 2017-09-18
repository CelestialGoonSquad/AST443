#Jasmine Garani, Lorena Mezini, Patrick Payne
#Start date 9/13/17
#Purpose: this code builds the bad pixel map for a master flat
# and it determines the ratio of warm and hot pixels to the total pixels

import numpy as np
from astropy.io import fits
import os
import warnings
from astropy.utils.exceptions import AstropyWarning
warnings.simplefilter('ignore',category=AstropyWarning)


#==========================================================================

jasminepath = "/Users/Jasmine/Documents/stony_brook/y4_sb/ast443/CGS-Groupdata/lab0/BigCCD/bigCCD-data/"
lorenapath = "/home/icecube/AST/CGS-GroupData/AST443/CGS-GroupData/lab0/BigCCD/bigCCD-data/"
patrickpath = "/Users/ilovealltigers/SBU_F17/AST_443/LAB1/CGS-GroupData/lab0/BigCCD/bigCCD-data/"

path = patrickpath

def badpixmapping(path):
    #Produces master flat array
    all_flats = []
    for f in os.listdir(path):
        if "flat" in f and "FIT" in f:
            hdulist = fits.open(path + '/' + f,ignore_missing_end=True)
            imagedata = hdulist[0].data
            norm_data = imagedata/np.median(imagedata)
            all_flats.append(norm_data)

        #Determines the median and normalizes
    master_flat = np.median(all_flats,axis=0)
    master_flat = master_flat/np.mean(master_flat)

        #Flattens master flat
    masterflatten=master_flat.flatten()

        #Calculates the standard deviation and mean    
    std = np.std(masterflatten)
    mean = np.mean(masterflatten)

        #Initialize bad pixel array
    badpix=np.zeros((1024,1024))

        #Calculates and assigns value of 0 to dead pixels, and 1 to undead pix
    for i in range(0,len(master_flat[0])):
        for k in range(0,len(master_flat[1])):
            if master_flat[i][k] <= mean - 5.*std:
                badpix[i][k]=0
            else:
                badpix[i][k]=1
        
    ###########################################################
        #Opens and reads in data
    filename = 'darks-expos300s-Neg10-Vis.00000000.DARK.FIT'
    hdulist2 = fits.open(path + '/' + filename)
    imagedata2 = hdulist2[0].data
    countvalues = imagedata2.flatten()
    cmax2 = 1150

        #Calculates mean and standard deviation
    meandark = np.mean(countvalues) #mean of single image
    sigdark = np.std(countvalues[countvalues<=cmax2]) #standard deviation of single image


       #Calculates and assigns value of 0 to the hot pixels, and preserves the dead pixels
    for i in range(0,len(imagedata2[0])):
        for k in range(0,len(imagedata2[1])):
            if imagedata2[i][k] >= meandark + 5.*sigdark or badpix[i][k] == 0: 
                badpix[i][k]=0
            else:
                badpix[i][k]=1
                
            #Writes out bad pixel map
    badpixmap = fits.PrimaryHDU(badpix)
    badpixmap.writeto('badpixmap-Neg05.fits',clobber=True)

#===================================EndOfFunction===========================================    

def warmhotratio(temp):
        #Imports and flattens data
    filename = 'darks-expos300s-' + temp + '-Vis.00000000.DARK.FIT'
    hdulist = fits.open(path + '/' + filename)
    imagedata = hdulist[0].data
    countvalues = imagedata.flatten()
    cmax = 1150

        #Calculation of the mean and standard deviation
    meandark = np.mean(countvalues) #mean of single image
    sigdark = np.std(countvalues[countvalues<=cmax]) #standard deviation of single image
                
        #Initializes warm and hot counts and ratios
    warmcount=0
    warmratio=0
    hotcount=0
    hotratio=0

        #Loops over the data and determines if a pixel is warm and/or hot
    for i in range(0,len(imagedata[0])):
        for k in range(0,len(imagedata[1])):
            if imagedata[i][k] >= meandark + 3.0*sigdark: 
                warmcount=warmcount+1
                if imagedata[i][k] >= meandark + 5.0*sigdark: 
                    hotcount=hotcount+1
    
        #Calculates the ratios compared to the total
    total=(1024.0)**2
    warmratio=warmcount/total
    hotratio=hotcount/total

        #Prints the desired values    
    print "Temperature: ", temp
    print "Warm Ratio: ", warmratio
    print "Hot Ratio: ", hotratio

    print "==========================================="





#===================================EndOfFunction===========================================    

warmhotratio("Neg5")
warmhotratio("Neg10")
badpixmapping(path)                

#THE END, i'll try harder next time :(


