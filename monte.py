# imports
import numpy as np
import matplotlib.pyplot as plt
import time
import random

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

def random_sampling(xmax=1.5,xmin=-2.5,ymax=1.5j,ymin=-1.5j, maxiter=100, samples = 1000, step = 0.01):

    # calculate x range, y range and area
    xrange = xmax - xmin
    yrange = ymax - ymin
    area = xrange * (yrange * -1j).real

    # timer for estimation purposes
    start = time.time()

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
        count += 1

    # calculate the estimated sample area
    sample_area = in_mandelbrot/samples * area
    # print(f'Time elapsed for sampling with s = {samples} , i = {maxiter} is {time.time() - start} seconds.')
    # print(f"Sample area = {sample_area}")
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

    xlist = []
    ylist = []
    in_mandelbrot = 0
    start = time.time()
    for s in range(samples):

        # take last strata in list
        xintv = x_strata.pop()
        yintv = y_strata.pop()

        # take a random number between the min and max from given strata
        xval = random.uniform(xintv[0], xintv[1])
        yval = random.uniform(yintv[0], yintv[1])

        # save computed (random) x- and y values in list for plotting purposes
        xlist.append(xval)
        ylist.append((yval*-1j).real)

        # create sample in complex plane
        sample = xval + yval

        # check if in mandelbrotset
        if calculation(sample, maxiter, simulation = True):
            in_mandelbrot +=1

    ylist = [y.real for y in ylist]
    sample_area = in_mandelbrot/samples * area
    # print(f'Time elapsed for LHS with s = {samples} , i = {maxiter} is {time.time() - start} seconds.')
    # print(f"Sample area = {sample_area}")

    if plot == True:
        plt.plot(xlist, ylist, 'o', markersize=1)
        plt.ylabel('Imaginary')
        plt.xlabel('Real')
        plt.title(f'Latin Hypercube Samples (s={samples})')
        plt.show()

        # save figure
        # plt.savefig('LHS_samples.png')

    return sample_area

