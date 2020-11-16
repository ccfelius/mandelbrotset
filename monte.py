# imports
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import math

def calculation(c,  maxiter = 1000, simulation=False, z = 0.0j):

    if not simulation:
        for i in range(maxiter):
            z = z * z + c
            # determine whether z is in mandelbrotset
            if np.sqrt((z.real * z.real) + (z.imag * z.imag)) >= 2:
                # return the amount of iterations needed to find out pixel not in mandelbrotset
                # return 0 if not in set
                return i, 0
            # return maximum amount of iterations for heatplot
            # return a 1 for counting purposes if in set
        return maxiter, 1

    else:
        for i in range(maxiter):
            z = z * z + c
            if np.sqrt((z.real * z.real) + (z.imag * z.imag)) >= 2:
                # return false if not in set
                return False
        # return true if in set
        return True


def mandelbrot(xmax=1.5,xmin=-2.5,ymax=1.5j,ymin=-1.5j, maxiter = 100, step=0.01):
    # define xrange, yrange and area
    xrange = xmax - xmin
    yrange = ymax - ymin
    area = xrange * (yrange * -1j).real

    # determine grid due to stepsize
    nx = int((xrange) / step)
    # convert y to real numbers
    ny = int(((yrange) / step * -1j).real)
    # declare matrix containing values for pixels
    m = np.zeros((ny, nx, 3))

    # # iy is rows, ix is cols
    start = time.time()
    pixels = 0
    cumsum = 0

    # for every 'pixel' (iy and ix) check whether in mandelbrotset
    for iy in range(ny):
        y_val = ymax - iy * step * 1j
        for ix in range(nx):
            # count all pixels in plot
            pixels += 1
            x_val = xmin + ix * step
            c = x_val + y_val
            m[iy, ix, 2], binary = calculation(c, maxiter)
            # count pixels that are in mandelbrotset
            cumsum += binary

    est_area = cumsum/pixels * area
    print(f'Time elapsed for estimating the mandelbrot area with i = {maxiter} is {time.time() - start} seconds.')
    print(f"Estimated area = {est_area}")
    return est_area


## Random Sampling

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

        # If antithetic variables are used
        else:
            # get invert of x and y samples
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


## Latin Hypercube Sampling

def LHS(xmax=1.5,xmin=-2.5,ymax=1.5j,ymin=-1.5j, maxiter=100, samples = 1000, plot = False):

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

    # Randomly shuffle x and y strata
    random.shuffle(x_strata)
    random.shuffle(y_strata)

    in_mandelbrot = 0
    for s in range(samples):

        # take last strata in list
        xintv = x_strata.pop()
        yintv = y_strata.pop()

        # take a random number between the min and max from given strata
        xval = random.uniform(xintv[0], xintv[1])
        yval = random.uniform(yintv[0], yintv[1])

        # create sample in complex plane
        sample = xval + yval

        # check if in mandelbrotset
        if calculation(sample, maxiter, simulation = True):
            in_mandelbrot +=1

    sample_area = in_mandelbrot/samples * area

    return sample_area


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

    # append x- and y intervals to strata
    for i in range(1, len(x)):
        x_strata.append([x[i - 1], x[i]])
        y_strata.append([y[i - 1], y[i]])

    # make a list with the indices of blocks (with length of x, y = sqrt(samples) for x and y-axis
    zx = np.arange(0, samples+math.sqrt(samples), math.sqrt(samples))
    zy = np.arange(0, samples, math.sqrt(samples))

    # define the intervals of indices (every sqrt(samples) there is an interval)
    intervals = []
    for i in range(1, len(zx)):
        intervals.append([int(zx[i-1]), int(zx[i])])

    # Keep track of available indices
    x_indices = [i for i in range(samples)]
    y_indices = [i for i in range(samples)]
    random.shuffle(x_indices)
    random.shuffle(y_indices)

    in_mandelbrot = 0
    # loop through indices defined in intervals
    for i in intervals:
        for j in intervals:
            # create lists from interval ranges
            x_temp = [x for x in range(j[0], j[1])]
            y_temp = [y for y in range(i[0], i[1])]

            # define x and y coordinate of sample
            cx = 0
            cy = 0

            # loop through available indices
            for k in x_indices:
                # if an available index is in slice of indices
                if k in x_temp:
                    # set x coordinate to available index
                    cx = k
                    # remove available index
                    x_indices.remove(k)
                    # break out of the for-loop
                    break

            # similar as above to determine y coordinate
            for k in y_indices:
                if k in y_temp:
                    cy = k
                    y_indices.remove(k)
                    break
                    # break out of for-loop and move to next block

            # from x-range, take strata with same x coordinate
            x_sample_range = x_strata[cx]
            # from y-range, take strata with same y coordinate
            y_sample_range = y_strata[-(cy+1)]

            # take a random number between the min and max from given strata
            xval = random.uniform(x_sample_range[0], x_sample_range[1])
            yval = random.uniform(y_sample_range[0], y_sample_range[1])

            # create sample in complex plane
            sample = xval + yval

            if calculation(sample, maxiter, simulation=True):
                in_mandelbrot += 1

    sample_area = in_mandelbrot / samples * area

    return sample_area

