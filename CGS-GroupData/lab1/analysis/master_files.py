import numpy as np
from astropy.io import fits
import warnings
from astropy.utils.exceptions import AstropyWarning
warnings.simplefilter('ignore',category=AstropyWarning)
import os


path = "/home/lmezini/lab1/"

def masterdark(path):
    all_darks = []
    for f in os.listdir(path):
        if "darks" in f and "FIT" in f:
            print f
            hdulist = fits.open(path + "/" + f,ignore_missing_end=True)
            header = hdulist[0].data
            imagedata = hdulist[0].data
            all_darks.append(imagedata)
    master_dark = np.median(all_darks,axis=0)
    darkhdu = fits.PrimaryHDU(master_dark)
    darkhdu.writeto('master_dark.fits',clobber=True)

def masterflat(path):
    all_flats = []
    for f in os.listdir(path):
        if "-flat" in f and "FIT" in f and "AUTODARK" not in f:
            print f
            hdulist = fits.open(path + '/' + f,ignore_missing_end=True)
            header = hdulist[0].header
            imagedata = hdulist[0].data
            norm_data = imagedata/np.median(imagedata)
            all_flats.append(norm_data)
    master_flat = np.median(all_flats,axis=0)
    master_flat = master_flat/np.mean(master_flat)
    flathdu = fits.PrimaryHDU(master_flat)                                    
    flathdu.writeto('master_flat.fits',clobber=True)  

masterdark(path)
masterflat(path)
