
# imports
import numpy as np
import matplotlib.pyplot as plt
import time

# Specify Initial Variables
xmax=1.5
xmin=-2.5
ymax=1.5j
ymin=-1.5j
# step=0.01
maxiter = 100

z = 0.0j
step = 0.005

def calculation(c, z = 0.0j, maxiter = 100):
    maxiter = 100
    for i in range(maxiter):
        z = z * z + c
        if np.sqrt((z.real * z.real) + (z.imag * z.imag)) >= 2:
            return i
    return maxiter


# start timer
start = time.time()

nx = int((xmax - xmin) / step)
ny = int(((ymax - ymin) / step * -1j).real)
m = np.zeros((ny, nx, 3))

for iy in range(ny):
    y_val = ymax - iy * step * 1j
    for ix in range(nx):
        x_val = xmin + ix * step

        c = x_val + y_val

        m[iy, ix, 0] = c.real
        m[iy, ix, 0] = c.imag
        m[iy, ix, 2] = calculation(c)

print(f'Elapsed time for step size = {step} is {time.time() - start} seconds...')

fig = plt.figure()
plt.imshow(m[:, :, 2], cmap='hot',
           extent=[xmin, xmax, (ymin * -1j).real, (ymax * -1j).real])
plt.ylabel('Imaginary')
plt.xlabel('Real')
plt.title('Mandelbrot Plot')

# save figure
# plt.savefig('Mandelbrot.png')

# show image
plt.show()

