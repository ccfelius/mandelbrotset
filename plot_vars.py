from monte import *
import scipy.stats as st
import math
import numpy as np

def MSE(array, mean):
    MSE = 0
    for i in array:
        MSE += (i - mean)**2
    return MSE / len(array)


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

simulations = 20
p_value = 0.95

def conduct_experiment(it, samples):
    outcomes = []
    for n in range(1, simulations+1):
        r_sampling = random_sampling(xmax, xmin, ymax, ymin, it, samples)
        # print(f"Simulation {n} gives an area of {r_sampling}")
        outcomes.append(r_sampling)

    MSE1 = MSE(outcomes, EX)
    print(f"Variance: {MSE1}")
    print(conf_int(EX, MSE1, simulations, p=0.95))
    return MSE1

# check MSE change for iterations increase
maxiters = np.array([100, 200, 300])
maxiter_MSEs= []
for it in maxiters:
    EX = mandelbrot(xmax, xmin, ymax, ymin, it) # gives 1.5139
    maxiter_MSEs.append(conduct_experiment(it, samples=10000))

plt.plot(maxiters, maxiter_MSEs)
plt.ylabel('MSE')
plt.xlabel('Number of iterations')
plt.title('MSE over iterations Plot')
plt.show()
plt.savefig('iterations.png')

# check MSE change for samples increase
samples = np.array([100, 1000, 10000, 100000])
samples_MSEs= []
maxiter= 100
for sample in samples:
    EX = mandelbrot(xmax, xmin, ymax, ymin, sample) # gives 1.5139
    samples_MSEs.append(conduct_experiment(maxiter, samples))

plt.plot(samples, samples_MSEs)
plt.ylabel('MSE')
plt.xlabel('Number of iterations')
plt.title('MSE over iterations Plot')
plt.show()
plt.savefig('samples.png')

