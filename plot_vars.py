from monte import *
import scipy.stats as st
import math
import numpy as np

# calculate the variance
def var(array, mean):
    var1 = 0
    for i in array:
        var1 += (i - mean)**2
    return var1 / len(array)

# calculate confidence interval
def conf_int(mean, var, n, p=0.95):
    pnew = (p+1)/2
    zval = st.norm.ppf(pnew)
    sigma = math.sqrt(var)
    alambda = (zval*sigma)/math.sqrt(n)
    min_lambda = mean - alambda
    plus_lambda = mean + alambda
    return f"Confidence interval: [{min_lambda} < X < {plus_lambda}] with p = {p}"

# Simulations initial values
z = 0.0j
step = 0.01
xmax= 0.5
xmin= -2.0
ymax= 1.1j
ymin= -1.1j

simulations = 50
p_value = 0.95

# run simulation
def conduct_experiment(it, samples):
    outcomes = []
    for n in range(1, simulations+1):
        r_sampling = random_sampling(xmax, xmin, ymax, ymin, it, samples)
        # print(f"Simulation {n} gives an area of {r_sampling}")
        outcomes.append(r_sampling)

    var1 = var(outcomes, EX)
    # print(f"Variance: {var1}")
    # print(conf_int(EX, var1, simulations, p=0.95))
    return var1

# check var change for iterations increase
maxiters = np.array([100, 200, 300, 400, 500])
maxiter_vars= []
for it in maxiters:
    EX = mandelbrot(xmax, xmin, ymax, ymin, it) 
    maxiter_vars.append(conduct_experiment(it, samples=10000))

plt.plot(maxiters, maxiter_vars)
plt.ylabel('Variance')
plt.xlabel('Number of iterations')
# plt.title('Variance over iterations Plot')
plt.show()
plt.savefig('iterations.png')
plt.close()

# check variance change for samples increase
samples = np.array([100, 1000, 10000, 100000])
samples_vars= []
maxiter = 200
for sample in samples:
    EX = mandelbrot(xmax, xmin, ymax, ymin, maxiter)
    samples_vars.append(conduct_experiment(maxiter, sample))

plt.xscale('log')
plt.plot(samples, samples_vars)
plt.ylabel('Variance')
plt.xlabel('Number of samples')
#plt.title('Variance over samples Plot')
#plt.show()
plt.savefig('samples.png')

