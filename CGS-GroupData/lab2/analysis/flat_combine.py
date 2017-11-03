#Jasmine Garani, Lorena Mezini, Patrick Payne
#Created 10/21/17
#Purpose: make master flat (not normalized)
#=====================================================================

import numpy as np
from astropy.io import fits
import os

#=====================================================================

jasminepath1 = "/home/jgarani/AST443/CGS-GroupData/lab2/usedata/" #path for flats with autodark
jasminepath2 = "/home/jgarani/AST443/CGS-GroupData/lab2/afterdark/" #path for flats with other darks applied
jasmineoutpath = "/home/jgarani/AST443/CGS-GroupData/lab2/combinedflats/" #path for output of flats

path1 = jasminepath1
path2 = jasminepath2
outpath = jasmineoutpath

#make master flat (not normalized) for neon spectrum flats
def masterflatneon(path,outpath):
    all_flatsneon = [] #make empty array for flats
    for f in os.listdir(path1): #find proper flats
        if 'flat-red' in f:
            print f
            hduflatsneon = fits.open(path + '/' + f,ignore_missing_end=True) #open flat
            flatdataneon = hduflatsneon[0].data
            all_flatsneon.append(flatdataneon) 
    master_flatneon = np.median(all_flatsneon,axis=0) #combine flats
    outflatneonhdu = fits.PrimaryHDU(master_flatneon)
    outflatneonhdu.writeto(outpath + '/' + 'master_flatneon.fits', overwrite=True) #write out master flat

#make master flat (not normalized) for neon spectrum flats
def masterflathg(path,outpath):
    all_flatshg = [] #make empty array for flats
    for f in os.listdir(path2): #find proper flats
        if 'flat-hg' in f:
            print f
            hduflatshg = fits.open(path + '/' + f,ignore_missing_end=True) #open flat
            flatdatahg = hduflatshg[0].data
            all_flatshg.append(flatdatahg) 
    master_flathg = np.median(all_flatshg,axis=0) #combine flats
    outflathghdu = fits.PrimaryHDU(master_flathg)
    outflathghdu.writeto(outpath + '/' + 'master_flathg.fits', overwrite=True) #write out master flat




#masterflatneon(path1,outpath)
masterflathg(path2,outpath)
