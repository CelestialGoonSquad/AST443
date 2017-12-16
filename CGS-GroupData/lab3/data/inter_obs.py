import numpy as np
#from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
#import csv

       #Names of interferometry files
names = ['Base-Single-70-00.txt','Base-Inter-30-12.txt','Base-Inter-35-11.txt','Base-Inter-40-09.txt','Base-Inter-45-18.txt','inter180-150-b65.txt','inter145-175-b70.txt','inter175-145-b75.txt']
       #lower bound on x axis
xlow  = [0.05,0.1,5,0.05,15,10,10]
xlow  = np.asarray(xlow)
       #upper bound on x axis
xhi   = [0.2,0.25,20,0.15,35,40,40]
xhi   = np.asarray(xhi)
       #lower bound on y axis
ylow  = [-0,0,-0,0,-0,0,-0]
       #upper bound on y axis
yhi   = [0.8,0.7,0.4,0.5,0.8,1.3,0.8]

    #interfereometry start angle
phistrt = [173,173,170,207,180,145,175]
phistrt = np.asarray(phistrt)
phistrt = (np.pi/180) * phistrt
    #Interferometry stop angle
phistop = [193,193,190,227,150,175,145]
phistop = np.asarray(phistop)
phistop = (np.pi/180) * phistop
    #altitude angle
alt = [28.98,28.88,28.62,29.40,0,0,0]
alt = np.asarray(alt)
alt = (np.pi/180) * alt
for i in range(0,2):
    name = names[i] 
    if 'Base' in name:  
        f_time = np.genfromtxt(name,skip_header=7,usecols = 0)
        f_pot = np.genfromtxt(name,skip_header=7,usecols = 1)
    if 'inter' in name:
        f_time = np.genfromtxt(name,skip_header=2,usecols=0)
        f_pot = np.genfromtxt(name,skip_header=2,usecols=1)
            
    background = np.where(f_time <= 2)
    background = background[0]
    backgrounda = []
    for index in background:
        backgrounda.append(f_pot[index])
    mean = np.mean(backgrounda)
    std = np.std(backgrounda)
    print mean, std

    #Calculation of x axis accordcing to radians not seconds
    phidiff = phistop[i]-phistrt[i]
    time = np.arange(0,phidiff,phidiff/len(f_time))
#    xlow = (phidiff/len(f_time)) * xlow
#    xhi  = (phidiff/len(f_time)) * xhi

    #Corrections for weird time problems
    if time[1] < 0:
        time = -1.0 * time
    if len(time) > len(f_time):
        problemindex=len(time)-1
        time = np.delete(time,problemindex)
        
    #Correction for altitude
    f_time = time#/np.cos(alt[i])


    f_pot = f_pot - mean
    f_pot = -1.0 * f_pot
    #Produce figure title and figure file name
    if '.txt' in name:
        figname = name.replace('.txt','.png')
        name = name.replace('.txt','')
        


    plt.plot(f_time,f_pot,label = "true")
    #plt.title(name)
    plt.xlabel("Position (radians)",fontsize=16)
    plt.ylabel("Voltage (V)",fontsize=16)
#    plt.xlim([xlow[i],xhi[i]])
#    plt.ylim([ylow[i],yhi[i]])
   # plt.legend()
    print figname
    plt.savefig(figname)
    plt.show()
