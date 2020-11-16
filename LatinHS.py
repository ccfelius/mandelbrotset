from mandelbrotset.monte import *
import numpy as np
import matplotlib.pyplot as plt
import time
import random

### INTENDED FOR TESTING FUNCTION SEPERATELY ###
### ALSO WITH VISUALISATION OF LATIN HYPERCUBE SAMPLES ###

## Simulations
z = 0.0j
step = 0.01
xmax= 0.5
xmin= -2.0
ymax= 1.1j
ymin= -1.1j
maxiter = 100
samples = 1000
simulations = 100


def LHS(xmax=1.5,xmin=-2.5,ymax=1.5j,ymin=-1.5j, maxiter=100, samples = 1000, plot = False):

    # calculate total area
    xrange = xmax - xmin
    yrange = ymax - ymin
    area = xrange * (yrange * -1j).real

    # define x-axis and y-axis
    x = np.linspace(xmin, xmax, samples+1)
    y = np.linspace((ymin*-1j).real, (ymax*-1j).real, samples+1)
    # make y values imaginary
    y = [(i * -1j) for i in y]
    y = y[::-1]

    # Define strata at x and y-axis
    x_strata = []
    y_strata = []
    for i in range(1, len(x)):
        x_strata.append([x[i - 1], x[i]])
        y_strata.append([y[i - 1], y[i]])

    # Randomly shuffle x and y strata
    random.shuffle(x_strata)
    random.shuffle(y_strata)

    xlist = []
    ylist = []
    in_mandelbrot = 0
    start = time.time()
    for s in range(samples):
        # take last strata in array
        xintv = x_strata.pop()
        yintv = y_strata.pop()

        # take a random number from the given strata
        xval = random.uniform(xintv[0], xintv[1])
        yval = random.uniform(yintv[0], yintv[1])

        # save computed x- and y values
        xlist.append(xval)
        ylist.append((yval*-1j).real)

        # create sample in complex plane
        sample = xval + yval

        # check if in mandelbrotset
        if calculation(sample, maxiter, simulation = True):
            in_mandelbrot +=1

    ylist = [y.real for y in ylist]
    sample_area = in_mandelbrot/samples * area
    print(f'Time elapsed for LHS with s = {samples} , i = {maxiter} is {time.time() - start} seconds.')
    print(f"Sample area = {sample_area}")

    if plot == True:
        plt.plot(xlist, ylist, 'o', markersize=1)
        plt.ylabel('Imaginary')
        plt.xlabel('Real')
        plt.title(f'Latin Hypercube Samples (s={samples})')
        plt.show()

        # save figure
        # plt.savefig('images/LHS/Mandelbrot.png')

    return sample_area, xlist, ylist


LHS(xmax, xmin, ymax, ymin, maxiter, samples=4, plot=True)
