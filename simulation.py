from mandelbrotset.monte import *
import scipy.stats as st
import math

def variance(array, mean):
    var = 0
    for i in array:
        var += (i - mean)**2
    return var / len(array)

def conf_int(mean, var, n, p=0.95):
    pnew = (p+1)/2
    zval = st.norm.ppf(pnew)
    sigma = math.sqrt(var)
    alambda = (zval*sigma)/math.sqrt(n)
    min_lambda = mean - alambda
    plus_lambda = mean + alambda
    return f"Confidence interval: [{min_lambda} < X < {plus_lambda}] with p = {p}"


## Simulations
z = 0.0j
step = 0.01
xmax= 0.5
xmin= -2.0
ymax= 1.1j
ymin= -1.1j

samples = 10000
simulations = 10
p_value = 0.95
maxiter = 200

EX = mandelbrot(xmax, xmin, ymax, ymin, maxiter) # gives 1.5139

outcomes = []
for n in range(1, simulations+1):
    r_sampling = random_sampling(xmax, xmin, ymax, ymin, maxiter, samples)
    print(f"Simulation {n} gives an area of {r_sampling}")
    outcomes.append(r_sampling)

var1 = variance(outcomes, EX)
print(f"Variance: {var1}")
print(conf_int(EX, var1, simulations, p=0.95))


