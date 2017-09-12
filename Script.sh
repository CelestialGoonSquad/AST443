#! /bin/bash
#comment
echo "Hello and welcome to the party!!!"

name=()    # planet name
rplanet=() # planet radius
rstar=()   # star radius
period=()  # orbital period (days)
incl=()       # inclination angle
semiax=()  # radius semi-major axis
mv=()      # star magnitude

numele=0   # number of array elements
i=0        # array index

datfile="exoplanet.eu_catalog.dat" # datafile to read from

echo $datfile

#-------------------------------------------------------------
### Evaluates planetary radius
awk -F '\t' '{print $9}' $datfile >> temp.dat # Prints values to temporary data file
sed -i -e 's/^$/NaN/' temp.dat                # Replaces empty data with NaN's
rplanet=( $(awk '{print $1}' temp.dat) )      # Assigns data to relevant array
\rm temp.dat                                  # Deletes temporary data file


numele=${#rplanet[@]}

for ((i=1;$i<$numele;i++))  # converts into km
do
    if [ "${rplanet[$i]}" = "NaN" ]; then # Checks for value to compute and creates array of unusable stars
	let ignore[$i]=1
    else
	let ignore[$i]=0
	rplanet[i]=`echo "${rplanet[$i]}*69911" | bc`
    fi
done
echo "Planetary Radius Array Built"
#echo "${rplanet[*]}"

#-------------------------------------------------------------
### Evaluates Initial Transit Time
awk -F '\t' '{print $37}' $datfile >> temp.dat
sed -i -e 's/^$/NoDate/' temp.dat
sed -i -e 's/ /-/g' temp.dat
tzero=( $(awk '{print $1}' temp.dat) )
\rm temp.dat


echo "Initial Transit Array Built"

#-------------------------------------------------------------
### Evaluates planet name
awk -F '\t' '{print $1}' $datfile >> temp.dat
sed -i -e 's/^$/NoName/' temp.dat
sed -i -e 's/ /-/g' temp.dat
name=( $(awk '{print $0}' temp.dat) )
\rm temp.dat

echo "Name Array Built"

#-------------------------------------------------------------
### Right Ascension
awk -F '\t' '{print $70}' $datfile >> temp.dat
sed -i -e 's/^$/-1.00/' temp.dat
ra=( $(awk '{print $1}' temp.dat) )
\rm temp.dat

echo "Right Ascension Array Built"

#-------------------------------------------------------------
### Declination
awk -F '\t' '{print $71}' $datfile >> temp.dat
sed -i -e 's/^$/-1.00/' temp.dat
dec=( $(awk '{print $1}' temp.dat) )
\rm temp.dat

for ((i=1;$i<$numele;i++))
do

    if (( $(echo "${dec[$i]} < 0" | bc -l) )); then
	ignore[$i]=1
    else
	ignore[$i]=0
    fi

done
echo "Declination Array Built"


#-------------------------------------------------------------
### Evaluates stellar radius
awk -F '\t' '{print $83}' $datfile >> temp.dat
sed -i -e 's/^$/NaN/' temp.dat
rstar=( $(awk '{print $1}' temp.dat) )
\rm temp.dat

for ((i=1;i<$numele;i++))  # converts into km
do
    if [ "${rstar[$i]}" = "NaN" ]; then
	let ignore[$i]=1
    else
	rstar[i]=`echo "${rstar[$i]}*695700" | bc`
    fi
done
echo "Stellar Radius Array Built"
#echo "${rstar[*]}"

#-------------------------------------------------------------
### Evaluates orbital period of planet, in hours
awk -F '\t' '{print $12}' $datfile >> temp.dat
sed -i -e 's/^$/NaN/' temp.dat
period=( $(awk '{print $1}' temp.dat) )
\rm temp.dat

for ((i=1;i<$numele;i++))  # checks for period value and converts to hours
do
    if [ "${period[$i]}" = "NaN" ]; then
	let ignore[$i]=1
    else
	day=24
	period[$i]=$(echo "${period[$i]}*$day"|bc -l)
    fi
done
echo "Period Array Built"
#echo "${period[*]}"

#-------------------------------------------------------------
### Evaluates inclination angle
awk -F '\t' '{print $21}' $datfile >> temp.dat
sed -i -e 's/^$/NaN/' temp.dat
incl=( $(awk '{print $1}' temp.dat) )
\rm temp.dat

#echo "${incl[*]}"
scale=6

convert=$(echo "3.14159265/180"|bc -l) 

#echo "$convert"

for ((i=1;i<$numele;i++))  # converts into radians
do
    if [ "${incl[$i]}" = "NaN" ]; then
	let ignore[$i]=1
    else
	incl[i]=`echo "${incl[$i]}*$convert" | bc`
    fi
done
echo "Inclination Angle Array Built"
#echo "${incl[*]}"

#-------------------------------------------------------------
### Evaluates semi-major axis
awk -F '\t' '{print $15}' $datfile >> temp.dat
sed -i -e 's/^$/NaN/' temp.dat
semiax=( $(awk '{print $1}' temp.dat) )
\rm temp.dat

#echo "${semiax[*]}"

for ((i=1;i<$numele;i++))  # converts into km 
do
    if [ "${semiax[$i]}" = "NaN" ]; then
	let ignore[$i]=1
    else
	semiax[i]=`echo "${semiax[$i]}*149600000" | bc`
    fi
done
echo "Semi-Major Axis Array Built"
#echo "${semiax[*]}"

#-------------------------------------------------------------
### Evaluates magnitude
awk -F '\t' '{print $72}' $datfile >> temp.dat
sed -i -e 's/^$/NaN/' temp.dat
mv=( $(awk '{print $1}' temp.dat) )
\rm temp.dat

magmin=12.5

for ((i=1;i<$numele;i++))  # checks for magnitude value
do
    if [ "${mv[$i]}" = "NaN" ]; then
	let ignore[$i]=1
	mv[$i]=130
    fi

    if (( $(echo "${mv[$i]} > $magmin" | bc -l) )); then
	ignoremagmin[$i]=1
    else
	ignoremagmin[$i]=0
    fi 
done
echo "Magnitude Array Built"
#echo "${mv[*]}"

#-------------------------------------------------------------
### Calculation of dimming magnitude
#-------------------------------------------------------------

dimmin=0.01

for ((i=1;i<$numele;i++))
do
    if [ ${ignore[$i]} == 0 ] && [ ${ignoremagmin[$i]} == 0 ] && [ "${rplanet[$i]}" != "NaN" ] && [ "${rstar[$i]}" != "NaN" ]; then
#	dimming[$i]=$(echo "${mv[$i]}*(${rplanet[$i]}^2/${rstar[$i]}^2)" | bc -l)
	dimming[$i]=$(echo "-2.5*(l(1-(${rplanet[$i]}^2/${rstar[$i]}^2))/l(10))"| bc -l) # -2.5 * ln(rplanet^2/rstar^2)/ln(10)
    else
	dimming[$i]=0
    fi

    if (( $(echo "${dimming[$i]} < $dimmin" | bc -l) )); then
	ignoredim[$i]=1
    else
	ignoredim[$i]=0
    fi

done
echo "Dimming Magnitude Array Built"
#echo "${dimming[*]}"


#-------------------------------------------------------------
### Calculation for Transit Period
#-------------------------------------------------------------

timemax=4.000


for ((i=1;i<$numele;i++))
do
    if [ ${ignore[$i]} == 0 ] && [ "${rplanet[$i]}" != "NaN" ] && [ "${rstar[$i]}" != "NaN" ]; then
	radii=$(echo "${rplanet[$i]}+${rstar[$i]}"|bc -l)
	squarert=$(echo "sqrt($radii^2)"|bc -l)
	    temp=$(echo "$squarert/${semiax[$i]}"|bc -l)
	    if (( $(echo "$temp < 1" | bc -l) )); then
		arcsin=$(echo "a($temp/sqrt(1-temp^2))"|bc -l)         # arcsin = arctan (x/sqrt(1-x^2))
		transit[$i]=$(echo "${period[$i]}*($arcsin/3.1415926535)"|bc -l)
	    else
		transit[$i]=15	
	    fi
    else
	transit[$i]=15
    fi

    if (( $(echo "${transit[$i]} > $timemax" | bc -l) )); then
	ignoretran[$i]=1
    else
	ignoretran[$i]=0
    fi

done
echo "Transit Duration Array Built"
#echo "${transit[*]}"

#-------------------------------------------------------------
### Printing Out Potential Planets & Transit Time Calculations
#-------------------------------------------------------------
date=`date '+%Y-%m-%d-%H:%M'`
candidatesfile=candidates-$date.out

JD=2458002.5

for ((i=1;i<$numele;i++))
do
    if [ ${ignoretran[$i]} == 0 ] && [ ${ignoredim[$i]} == 0 ] && [ "${tzero[$i]}" != "NaN" ] && [ "${period[$i]}" != "NaN" ]; then
	echo "$i --- Name: ${name[$i]}, Transit Duration: ${transit[$i]}, Dimming Magnitude: ${dimming[$i]}," >> $candidatesfile
	echo "        Right Ascension: ${ra[$i]}, Declination: ${dec[$i]}, Period: ${period[$i]}" >> $candidatesfile

	elapsed=$(echo "(${tzero[$i]})-($JD)" |bc -l)
#	orbitsint=$(echo "(${elapsed[$i]})/(${period[$i]})" |bc)
#	lastorb=$(echo "(${period[$i]})*(${orbitsint[$i]})" |bc -l)
 #     	monthorbs=$(echo "(720)/(${period[$i]})" |bc)

	for ((k=1;k<$monthorbs;k++))
	do
#	    transtime=`echo "(${lastorb[$i]})+($k)*(${period[$i]})" |bc -l`
#	    transtime=`echo "($transtime)+(0.01666666666666667)" |bc -l`
	    echo "      $k --- $transtime" >> $candidatesfile
	done
	echo "------------------------------------------------------------------------------" >> $candidatesfile
    fi
done
echo "Candidates written to $candidatesfile"

