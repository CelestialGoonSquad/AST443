#! /bin/bash
#RA = "300.182"
#DEC = "+22.709" 
for file in $(ls -1 *.cat); do
    grep "300" ${file} | while read -r A B C D; do #A=RA B=DEC C=flux D=Error 
    if (( $(echo "$A > 300.1805" |bc -l) )) && (( $(echo "$A < 300.1825" |bc -l) ));then
	if (( $(echo "${B:1:-1} > 22.70" |bc -l) )) && (( $(echo "${B:1:-1} < 22.72" |bc -l) )); then
	    echo ${file}
	    echo ${file} $A $B $C $D >> hd189733_time_flux.txt
	fi
    fi
    done
done
