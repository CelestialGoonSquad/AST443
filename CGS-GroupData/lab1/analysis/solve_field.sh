#!/bin/bash -u

for file in $(ls -1 *.FIT)
do
   echo ${file}
   solve-field --ra 300.1792 --dec 22.7108 --radius 1 ${file}  
done
