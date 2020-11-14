
# imports
import numpy as np
import matplotlib.pyplot as plt
import time
import random

# Specify Initial Variables
xmax=0.5
xmin=-2.0
ymax=1.1j
ymin=-1.1j
# step=0.01
# maxiter = 100
z = 0.0j
step = 0.01

def calculation(c, z = 0.0j, maxiter = 5):

    maxiter = 200
    for i in range((maxiter)):
        z = z * z + c
        if np.sqrt((z.real * z.real) + (z.imag * z.imag)) >= 2:
            return i
    return maxiter

# start timer
start = time.time()

nx = int((xmax - xmin) / step)
print(nx)
ny = int(((ymax - ymin) / step * -1j).real)
print(ny)
rnx = range(nx)
rny = range(ny)
m = np.zeros((ny, nx, 3))
samples = 100000

for s in range(samples):
    iy = random.choice(rny)
    ix = random.choice(rnx)
    y_val = ymax - iy * step * 1j
    x_val = xmin + ix * step
    c = x_val + y_val

    # m[iy, ix, 0] = c.real
    # m[iy, ix, 0] = c.imag
    m[iy, ix, 2] = calculation(c)

# print(m)
# print(len(m))
# print(m[:,:,2])

# f = open("demofile3.txt", "w")
# counter = 0
# for line in m[:,:,2]:
#     f.write(str(line)+ "\n")
#     counter +=1
# f.close()

# print(len(m[:,:,2][0]))
# print("output is this " + str(counter))
print(f'Elapsed time for step size = {step} is {time.time() - start} seconds... x')

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

print("done")