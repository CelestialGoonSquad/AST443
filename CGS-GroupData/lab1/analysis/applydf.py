import numpy as np
from astropy.io import fits
import os
import warnings
from astropy.utils.exceptions import AstropyWarning
warnings.simplefilter('ignore',category=AstropyWarning)

lorenapath = "/home/lmezini/AST443/CGS-GroupData/lab1/"
lorenanewpath = "/home/lmezini/AST443/CGS-GroupData/lab1/calibration/"
jasminepath = '/home/jgarani/AST443/CGS-GroupData/lab1/raw-data/'
jasminenewpath = '/home/jgarani/AST443/CGS-GroupData/lab1/calibration/'


path = jasminepath
newpath = jasminenewpath

def applydf(path,newpath):
    all_files = []
    dark_hdulist = fits.open("master_dark.fits")
    dark_data = dark_hdulist[0].data
    flat_hdulist = fits.open("master_flat.fits")
    flat_data = flat_hdulist[0].data
    
    #list with bad files
    badfiles = ['L1-sci.00000063.FIT','L1-sci.00000094.FIT','L1-sci.00000197.FIT','L1-sci.00000537.FIT','L1-sci.00000550.FIT','L1-sci.00000551.FIT','L1-sci.00000552.FIT','L1-sci.00000553.FIT','L1-sci.00000554.FIT','L1-sci.00000555.FIT','L1-sci.00000556.FIT','L1-sci.00000557.FIT','L1-sci.00000558.FIT','L1-sci.00000559.FIT','L1-sci.00000560.FIT','L1-sci.00000565.FIT']
    
    df_sci_a = []  #array of all the reduced science images

    for f in os.listdir(path):
        if "sci" in f and f not in badfiles:
            print f
            hdulist = fits.open(path + '/' + f, ignore_missing_end=True)
            header = hdulist[0].header
            imagedata = hdulist[0].data
            df_sci = (imagedata-dark_data)/flat_data
            bdf_sci = applybadpix(path,newpath,df_sci)
            print type(bdf_sci)
            print bdf_sci.shape
            newhdu = fits.PrimaryHDU(bdf_sci)
            newhdu.writeto(newpath+ '/bdf-'+f,clobber=True)
            break
def applybadpix(path,newpath,df_sci):
    badpixmaphdulist = fits.open('badpixmap.fits')  #open bad pixel map
    badpixmap = badpixmaphdulist[0].data   #extract data for bad pixel map
    bploc = np.where(badpixmap == 0)  #locations of bad pixels in map
    bplocx = bploc[0]  #x locations of bad pixels
    bplocy = bploc[1]  #y locations of bad pixels
    print bploc
    for index in range(0,len(bplocx)):
        df_sci[bplocx[index]][bplocy[index]] = 0
    print df_sci
    print type(df_sci)
    return df_sci


applydf(path,newpath)

