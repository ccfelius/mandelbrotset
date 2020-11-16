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

# amount of samples has to be a int if square root!
# in orther for orthogonal sampling to work
samples = 144
simulations = 20
p_value = 0.95
maxiter = 200

EX = mandelbrot(xmax, xmin, ymax, ymin, maxiter) # gives 1.5139

# Simulations
rs_samples = []
lhs_samples = []
orth_samples = []
for n in range(1, simulations+1):
    r_sampling = random_sampling(xmax, xmin, ymax, ymin, maxiter, samples)
    lhs_sim = LHS(xmax, xmin, ymax, ymin, maxiter, samples, plot=False)
    orth_sim = orthogonal_sampling(xmax, xmin, ymax, ymin, maxiter, samples, plot=False)
    print(f"Simulation {n}, s={samples}, i={maxiter}, RS: {r_sampling}, LHS: {lhs_sim}, Orthogonal: {orth_sim}")
    rs_samples.append(r_sampling)
    lhs_samples.append(lhs_sim)
    orth_samples.append(orth_sim)
#
var1 = variance(rs_samples, EX)
var2 = variance(lhs_samples, EX)
var3 = variance(orth_samples, EX)

print(f"\nEstimated Mandelbrot Area {EX}")
print(f"Simulations: {simulations}, Samples: {samples}\nVariance RS: {var1}\nVariance LHS: {var2}\nVariance Orthogonal Sampling: {var3}\n ")
print(f"Estimated Mandelbrot Area E[X]: {EX}")
print(conf_int(EX, var1, simulations, p=0.95))
print(conf_int(EX, var2, simulations, p=0.95))
print(conf_int(EX, var3, simulations, p=0.95))



