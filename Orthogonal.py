from mandelbrotset.monte import *
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import math

### INTENDED FOR TESTING FUNCTION SEPERATELY ###
### ALSO WITH VISUALISATION OF ORTHOGONAL SAMPLES ###

## Simulations
z = 0.0j
step = 0.01
xmax= 0.5
xmin= -2.0
ymax= 1.1j
ymin= -1.1j
maxiter = 100

# samples has to be a integer when sqrt
samples = 4
simulations = 1


def orthogonal_sampling(xmax=1.5,xmin=-2.5,ymax=1.5j,ymin=-1.5j, maxiter=100, samples = 1000, plot = False):

    # calculate total area
    xrange = xmax - xmin
    yrange = ymax - ymin
    area = xrange * (yrange * -1j).real

    # define x-axis and y-axis
    x = np.linspace(xmin, xmax, samples+1)
    # convert to real-values in order for linspace to deal with imaginary numbers
    y = np.linspace((ymin*-1j).real, (ymax*-1j).real, samples+1)
    # make y values imaginary again
    y = [(i * -1j) for i in y]
    # reverse list as - becomes +
    y = y[::-1]

    # Define strata at x and y-axis
    x_strata = []
    y_strata = []
    for i in range(1, len(x)):
        x_strata.append([x[i - 1], x[i]])
        y_strata.append([y[i - 1], y[i]])

    # define empty matrix to see where we need to sample
    # just to check whether orthogonal sampling works ok
    A = np.zeros(samples ** 2).reshape(samples, samples)
    zx = np.arange(0, samples+math.sqrt(samples), math.sqrt(samples))
    zy = np.arange(0, samples, math.sqrt(samples))

    intervals = []
    for i in range(1, len(zx)):
        intervals.append([int(zx[i-1]), int(zx[i])])

    # Keep track of available indices
    x_indices = [i for i in range(samples)]
    y_indices = [i for i in range(samples)]
    random.shuffle(x_indices)
    random.shuffle(y_indices)
    # intervals of indices

    xlist = []
    ylist = []

    in_mandelbrot = 0
    start = time.time()
    for i in intervals:
        for j in intervals:
            x_temp = [x for x in range(j[0], j[1])]
            y_temp = [y for y in range(i[0], i[1])]
            cx = 0
            cy = 0
            for k in x_indices:
                if k in x_temp:
                    cx = k
                    x_indices.remove(k)
                    break
            for k in y_indices:
                if k in y_temp:
                    cy = k
                    y_indices.remove(k)
                    break

            # add 1 to orthogonal matrix where sample is taken from
            A[cy][cx] = 1

            # sample:
            x_sample_range = x_strata[cx]
            y_sample_range = y_strata[-(cy+1)]

            # take a random number between the min and max from given strata
            xval = random.uniform(x_sample_range[0], x_sample_range[1])
            yval = random.uniform(y_sample_range[0], y_sample_range[1])

            # save computed (random) x- and y values in list for plotting purposes
            xlist.append(xval)
            ylist.append((yval * -1j).real)

            # create sample in complex plane
            sample = xval + yval

            # print(x_sample_range, y_sample_range)
            # if you uncomment the statements you print the blocks
            print(A[(i[0]):(i[1]), (j[0]):(j[1])])
            print()

            if calculation(sample, maxiter, simulation=True):
                in_mandelbrot += 1

    # Uncommit if you want to see the orthogonal matrix
    print(A)
    ylist = [y.real for y in ylist]
    sample_area = in_mandelbrot / samples * area
    print(f'Time elapsed for Orthogonal Sampling with s = {samples} , i = {maxiter} is {time.time() - start} seconds.')
    print(f"Sample area = {sample_area}")

    if plot == True:
        plt.plot(xlist, ylist, 'o', markersize=6)
        plt.ylabel('Imaginary')
        plt.xlabel('Real')
        plt.title(f'Orthogonal Sampling (s={samples})')
        plt.show()

        # save figure
        plt.savefig('Orthogonal.png')

    return sample_area

orthogonal_sampling(xmax, xmin, ymax, ymin, maxiter, samples, plot = True)
