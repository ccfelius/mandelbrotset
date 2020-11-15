# imports
import numpy as np
import matplotlib.pyplot as plt
import time
import random

def calculation(c,  maxiter = 1000, simulation=False, z = 0.0j):

    if not simulation:
        for i in range(maxiter):
            z = z * z + c
            if np.sqrt((z.real * z.real) + (z.imag * z.imag)) >= 2:
                return i, 0
        return maxiter, 1

    else:
        for i in range(maxiter):
            z = z * z + c
            if np.sqrt((z.real * z.real) + (z.imag * z.imag)) >= 2:
                return False
        return True


def mandelbrot(xmax=1.5,xmin=-2.5,ymax=1.5j,ymin=-1.5j, maxiter = 100, step=0.01):
    xrange = xmax - xmin
    yrange = ymax - ymin
    area = xrange * (yrange * -1j).real
    nx = int((xrange) / step)
    ny = int(((yrange) / step * -1j).real)
    m = np.zeros((ny, nx, 3))

    # # iy is rows, ix is cols
    start = time.time()
    pixels = 0
    cumsum = 0
    for iy in range(ny):
        y_val = ymax - iy * step * 1j
        for ix in range(nx):
            pixels += 1
            x_val = xmin + ix * step
            c = x_val + y_val
            m[iy, ix, 2], binary = calculation(c, maxiter)
            cumsum += binary

    est_area = cumsum/pixels * area
    print(f'Time elapsed for estimating the mandelbrot area with i = {maxiter} is {time.time() - start} seconds.')
    print(f"Estimated area = {est_area}")
    return est_area


# Random Sampling

def random_sampling(xmax=1.5,xmin=-2.5,ymax=1.5j,ymin=-1.5j, maxiter=100, samples = 1000, step = 0.01):
    xrange = xmax - xmin
    yrange = ymax - ymin
    area = xrange * (yrange * -1j).real
    start = time.time()
    in_mandelbrot = 0
    count = 0

    while count < samples:
        y_sample = random.uniform(ymin, ymax)
        x_sample = random.uniform(xmin, xmax)
        sample = x_sample + y_sample

        # check if in mandelbrotset
        if calculation(sample, maxiter, simulation = True):
            in_mandelbrot +=1
        count += 1

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
    # print(f'Time elapsed for LHS with s = {samples} , i = {maxiter} is {time.time() - start} seconds.')
    # print(f"Sample area = {sample_area}")

    if plot == True:
        plt.plot(xlist, ylist, 'o', markersize=1)
        plt.ylabel('Imaginary')
        plt.xlabel('Real')
        plt.title(f'Latin Hypercube Samples (s={samples})')
        plt.show()

        # save figure
        # plt.savefig('images/LHS/Mandelbrot.png')

    return sample_area, xlist, ylist

