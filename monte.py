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
        nx = int((xrange) / step)
        for ix in range(nx):
            # create random sample in complex plane
            y_sample = random.uniform(ymin, ymax)
            x_val = xmin + ix * step
            sample = x_val + y_sample

            # check if in mandelbrotset
            if calculation(sample, maxiter, simulation = True):
                in_mandelbrot +=1
            count += 1

    sample_area = in_mandelbrot/samples * area
    # print(f'Time elapsed for sampling with s = {samples} , i = {maxiter} is {time.time() - start} seconds.')
    # print(f"Sample area = {sample_area}")
    return sample_area


# Latin Hypercube Sampling

# def LHS(xmax=1.5,xmin=-2.5,ymax=1.5j,ymin=-1.5j, maxiter=100, samples = 1000, step = 0.01):
#     xrange = xmax - xmin
#     yrange = ((ymax - ymin) * -1j).real
#     area = xrange * yrange
#     xgrid = int(xrange/(1/samples))
#     ygrid = int(y/(1/samples))
#     start = time.time()
#     in_mandelbrot = 0
#     count = 0
#
#     while count < samples:
#         # create random sample in complex plane
#         y_sample = random.uniform(ymin, ymax)
#         nx = int((xrange) / step)
#         for ix in range(nx):
#             x_val = xmin + ix * step
#             sample = x_val + y_sample
#
#             # check if in mandelbrotset
#             if calculation(sample, maxiter, simulation = True):
#                 in_mandelbrot +=1
#             count += 1

