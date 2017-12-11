This file outlines what everything in this directory is for.

There are 7 text files that are the 7 different baselines that are used. These are listed below
Base-Inter-30-12.txt
Base-Inter-35-11.txt
Base-Inter-40-09.txt
Base-Inter-45-18.txt
inter180-150-b65.txt
inter145-175-b70.txt
inter175-145-b75.txt

The first 4 are ours, the last three are from rachel, the first two numbers are the azimuthal angles they slewed from, and the number after the b is the baseline

All of these baselines aren't the actual baseline, it is the distance in inches from the center, you must double these numbers to get the baseline in inches to use for the rest of the calulations

inter_obs.py This file is used to plot the text files listed above for time on the x-axis and the potential of the y-axis

inter_visvsbase.py This file is used to plot the visibilities vs. the baselines, it uses data from file: bsnvs.txt, which has the baselines and the visibilities. The visibilities should be fine, but we need the actual baselines, which should B_{\lambda} This code also does the fitting of the sinc function.


For the single dish observations, all the code is in sing_dish_obs.py, and the plot is single_dish_plot.png
