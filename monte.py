# imports
import numpy as np
import matplotlib.pyplot as plt
import time
import random

maxiter = 1000
z = 0.0j
step = 0.005
xmax= 0.5
xmin= -2.0
ymax= 1.1j
ymin= -1.1j
xrange = xmax - xmin
yrange = ymax - ymin
area = xrange*(yrange*-1j).real

def estimation_area():
    # we need to create a function that estimates the area of the mandelbrot
    # iets met pixels in mandelbrot en erbuiten?

    #### STEPS:
    # Calculate # pixels (all combinations of nx, ny
    # Calculate # pixels in mandelbrot

    # dan is als het goed is de area van mandelbrot geschat?
    return 0


def calculation(c,  maxiter = 1000, simulation=False, z = 0.0j):

    if not simulation:
        for i in range(maxiter):
            z = z * z + c
            if np.sqrt((z.real * z.real) + (z.imag * z.imag)) >= 2:
                return i, 1
        return maxiter, 0

    else:
        for i in range(maxiter):
            z = z * z + c
            if np.sqrt((z.real * z.real) + (z.imag * z.imag)) >= 2:
                return False
        return True


def mandelbrot(xmax=1.5,xmin=-2.5,ymax=1.5j,ymin=-1.5j, maxiter = 100, step=0.01):
    nx = int((xmax - xmin) / step)
    ny = int(((ymax - ymin) / step * -1j).real)
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

    print(f"Total pixels: {pixels}")
    est_area = cumsum/pixels * area
    print(f'Time elapsed for estimating the area with i = {maxiter} is {time.time() - start} seconds.')
    print(f"Estimated area = {est_area}")
    return est_area


def random_sampling(xmax=1.5,xmin=-2.5,ymax=1.5j,ymin=-1.5j, maxiter=100, samples = 1000):
    start = time.time()
    in_mandelbrot = 0
    count = 0

    while count < samples:
        # create random sample
        y_sample = random.uniform(ymin, ymax)
        x_sample = random.uniform(xmin, xmax)
        sample = x_sample + y_sample

        # check if in mandelbrotset
        if calculation(sample, maxiter, simulation = True):
            in_mandelbrot +=1
        count += 1

    sample_area = in_mandelbrot/samples * (xrange*(yrange*-1j).real)
    # print(in_mandelbrot, samples, xrange*(yrange*-1j).real)
    print(f'Time elapsed for sampling with s = {samples} , i = {maxiter} is {time.time() - start} seconds.')
    print(f"Sample area = {sample_area}")
    return sample_area

samples = 10000
r_sampling = random_sampling(xmax, xmin, ymax, ymin, maxiter, samples)
m_estimation = mandelbrot(xmax, xmin, ymax, ymin, maxiter)

