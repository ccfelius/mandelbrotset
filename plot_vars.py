from monte import *
import scipy.stats as st
import math
import numpy as np


# calculate confidence interval
def conf_int(mean, var, n, p=0.95):
    pnew = (p+1)/2
    zval = st.norm.ppf(pnew)
    sigma = math.sqrt(var)
    alambda = (zval*sigma)/math.sqrt(n)
    min_lambda = mean - alambda
    plus_lambda = mean + alambda
    return min_lambda, plus_lambda


# Simulations initial values
z = 0.0j
step = 0.01
xmax= 0.5
xmin= -2.0
ymax= 1.1j
ymin= -1.1j

p_value = 0.95 

# run simulation
def conduct_experiment(it, samples, simulations):
    outcomes = []
    for n in range(1, simulations+1):
        r_sampling = random_sampling(xmax, xmin, ymax, ymin, it, samples)
        outcomes.append(r_sampling)
    
    return outcomes

#################

# check errors change for iterations increase
simulations = 20
maxiters =  np.arange(100, 5001, 100).tolist()
errors = []
samples = 5000
max_i = np.mean(conduct_experiment(5000, samples, simulations))
print(max_i)
id
for it in maxiters:
    print(it)
    errors.append((abs(np.mean(conduct_experiment(it, samples, simulations)) - max_i)))


plt.plot(maxiters, errors)
plt.ylabel('Error')
plt.xlabel('Number of iterations')
plt.show()
plt.savefig('iterations.png')
plt.close()

##########################

# check mean change for samples increase

simulations = 20
samples = np.arange(100, 10001, 100).tolist() 
samples_mean, ci_lower, ci_higher = [], [], []
maxiter = 200

for sample in samples:
    print(sample)
    outcomes= (conduct_experiment(maxiter, sample, simulations))
    mean= np.mean(outcomes)
    samples_mean.append(mean)
    lower, higher = conf_int(np.mean(outcomes), np.var(outcomes), len(outcomes), p=0.95)
    ci_lower.append(lower)
    ci_higher.append(higher)

plt.plot(samples, samples_mean)
plt.fill_between(samples, ci_lower, ci_higher, color='b', alpha=.1)

plt.ylabel('Mean')
plt.xlabel('Number of samples')
plt.show()
plt.savefig('samples.png')
plt.close()

# #################

# check mean change for simulations increase
simulations_mean, ci_lower, ci_higher = [], [], []
samples = 1000
maxiter = 200
simulations = np.arange(100, 3001, 100).tolist() 

for i in simulations:
    print(i)
    outcomes= (conduct_experiment(maxiter, samples, i))
    mean = np.mean(outcomes)
    simulations_mean.append(mean)
    lower, higher = conf_int(np.mean(outcomes), np.var(outcomes), len(outcomes), p=0.95)
    ci_lower.append(lower)
    ci_higher.append(higher)

plt.plot(simulations, simulations_mean)
plt.fill_between(simulations, ci_lower, ci_higher, color='b', alpha=.1)

plt.ylabel('Mean')
plt.xlabel('Number of simulations')
plt.show()
plt.savefig('simulations.png')
plt.close()
