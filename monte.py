#Monte carlo integration
import math
import random

# misschien beter om gewoon de code van main.py te linken
def function(x):
    z = 0.0j 
    ....
    return z * z + c

count = 0
in_area = 0

while count < 1000000:
    # ik had maar even in het figuur gekeken en dit waren ongeveer waarbinnen de mandelbrot zit
    y_coord = random.uniform(-1.14935, 1.13149)
    x_coord = random.uniform(-1.99655, 0.491665)

    # check if generated coordinate is in mandelbrot
    if y_coord < function(x_coord):
        in_area += 1
        
    count += 1

    area_box = 9/ math.e
    print(in_area/count)* area_box