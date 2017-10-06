#!/bin/bash

for file in $(ls -1 *.FIT)
do
    solve-field --ra 300.1792 --dec 22.7108 --radius 1 ${file}  # complete this line with your call to solve-field
done
