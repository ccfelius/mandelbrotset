# imports
import numpy as np
import matplotlib.pyplot as plt
import time
import random


maxiter = 100
z = 0.0j
step = 0.005

def calculation(c, z = 0.0j, maxiter = 100):
    maxiter = 100
    for i in range(maxiter):
        z = z * z + c
        if np.sqrt((z.real * z.real) + (z.imag * z.imag)) <= 2:
            return True
    return False


count = 0
in_mandelbrot = 0

while count < 1000000:
    # create random sample
    y_sample = random.uniform(-1.5j, 1.5j)
    x_sample = random.uniform(-2.5, 1.5)
    sample = x_sample + y_sample

    # check if in mandelbrotset
    if calculation(sample)==True:        
        in_mandelbrot +=1

    count += 1

print(in_mandelbrot)
print(in_mandelbrot / count * 3000)
