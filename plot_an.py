"""
This code is used to plot the results of figure 4
It plots the variance when increasing the number of samples 
using the antithetic method
"""

import scipy.stats as st
import math
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import math
from monte import *


#function from antithetic.py
def random_sampling(xmax=1.5,xmin=-2.5,ymax=1.5j,ymin=-1.5j, maxiter=100, samples = 1000, step = 0.01, antithetic=False):
    # calculate x range, y range and area
    xrange = xmax - xmin
    yrange = ymax - ymin
    area = xrange * (yrange * -1j).real

    in_mandelbrot = 0
    count = 0
    # for all samples, sample a random y and x value
    while count < samples:
        #note that ymin and ymax are complex numbers
        y_sample = random.uniform(ymin, ymax)
        x_sample = random.uniform(xmin, xmax)
        sample = x_sample + y_sample

        # check if in mandelbrotset
        if calculation(sample, maxiter, simulation = True):
            in_mandelbrot +=1

        if not antithetic:
            count += 1

        else:
            ay_sample = (ymin+ymax) - y_sample
            ax_sample = (xmin+xmax) - x_sample
            sample2 = ax_sample + ay_sample

            # check if in mandelbrotset
            if calculation(sample2, maxiter, simulation = True):
                in_mandelbrot +=1

            count += 2

        # calculate the estimated sample area
    sample_area = in_mandelbrot / samples * area

    return sample_area


# run simulation and with antithetic and return outcomes
def conduct_experiment(it, samples, simulations, antithetic=False):
    outcomes = []
    for n in range(1, simulations+1):
        r_sampling = random_sampling(xmax, xmin, ymax, ymin, maxiter, samples, antithetic=False)
        outcomes.append(r_sampling)
    return outcomes

# Simulations initial values
z = 0.0j
step = 0.01
xmax= 0.5
xmin= -2.0
ymax= 1.1j
ymin= -1.1j

simulations = 1900
maxiter = 200
samples = np.arange(1, 51, 1).tolist()
samples_var = []



# run simulation various sample values calculate variance and
# calculate confidence intervals
for sample in samples:
    print(sample)
    outcomes = (conduct_experiment(maxiter, sample, simulations, antithetic=True))
    var1 = np.var(outcomes)
    samples_var.append(var1)



# def conduct_experiment_normal(it, samples, simulations):
#     outcomes = []
#     for n in range(1, simulations+1):
#         r_sampling = random_sampling(xmax, xmin, ymax, ymin, maxiter, samples)
#         outcomes.append(r_sampling)
#     return outcomes


samples_var_normal = []
# run simulation various sample values calculate variance and
# calculate confidence intervals
for sample in samples:
    print(sample)
    outcomes = (conduct_experiment(maxiter, sample, simulations, antithetic=False))
    var1 = np.var(outcomes)
    samples_var_normal.append(var1)


# plot figure
plt.plot(samples, samples_var, label = "Antithetic", alpha=1)
plt.plot(samples, samples_var_normal, label = "No antithetic", alpha=.5)
plt.legend()
plt.ylabel('Variance')
plt.xlabel('Number of samples')
plt.show()
plt.close()
