# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 20:53:25 2017

@author: Jasmine
"""

import numpy as np
import matplotlib.pyplot as plt

with open("all-images.cal.txt") as f:
    lines = f.readlines()
    x = [line.split()[0] for line in lines]
    y = [line.split()[1] for line in lines]

print x
print y

plt.plot(x,y)
plt.show()
