from mandelbrotset.monte import *
import scipy.stats as st
import math

def conf_int(mean, var, n, p=0.95):
    pnew = (p+1)/2
    zval = st.norm.ppf(pnew)
    sigma = math.sqrt(var)
    alambda = (zval*sigma)/math.sqrt(n)
    min_lambda = mean - alambda
    plus_lambda = mean + alambda
    return f"Confidence interval: [{min_lambda:.4f} < X < {plus_lambda:.4f}] with p = {p}"

### Control Variets ###

## Simulations
z = 0.0j
step = 0.01
xmax= 0.5
xmin= -2.0
ymax= 1.1j
ymin= -1.1j

# amount of samples has to be a int if square root!
# in orther for orthogonal sampling to work
samples = 1024
simulations = 40
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

print("NORMAL ESTIMATES: ")


print(f"\nEstimated Mandelbrot Area {EX}")
print(f"Simulations: {simulations}, Samples: {samples}\nVariance RS: {np.var(rs_samples)}\nVariance LHS: {np.var(lhs_samples)}\nVariance Orthogonal Sampling: {np.var(orth_samples)}\n ")
print(f"Estimated Mandelbrot Area E[X]: {EX:.4f}")
print(conf_int(EX, np.var(rs_samples), simulations, p=0.95))
print(conf_int(EX, np.var(lhs_samples), simulations, p=0.95))
print(conf_int(EX, np.var(orth_samples), simulations, p=0.95))

print()
print("CONTROL VARIATES ESTIMATES: ")

mid = int(simulations/2)
cv_rs_x = rs_samples[:mid]
cv_rs_y = rs_samples[mid:]
cv_lhs_x = lhs_samples[:mid]
cv_lhs_y = lhs_samples[mid:]
cv_orth_x = orth_samples[:mid]
cv_orth_y = orth_samples[mid:]

cv_rs = [a_i - b_i + EX for a_i, b_i in zip(cv_rs_x, cv_rs_y)]
cv_lhs = [a_i - b_i + EX for a_i, b_i in zip(cv_lhs_x, cv_lhs_y)]
cv_orth = [a_i - b_i + EX for a_i, b_i in zip(cv_orth_x, cv_orth_y)]

print(f"\nEstimated Mandelbrot Area {EX}")
print(f"Simulations: {simulations}, Samples: {samples}\nVariance RS: {np.var(cv_rs)}\nVariance LHS: {np.var(cv_lhs)}\nVariance Orthogonal Sampling: {np.var(cv_orth)}\n ")
print(f"Estimated Mandelbrot Area E[X]: {EX:.4f}")
print(conf_int(EX, np.var(cv_rs), simulations, p=0.95))
print(conf_int(EX, np.var(cv_lhs), simulations, p=0.95))
print(conf_int(EX, np.var(cv_orth), simulations, p=0.95))
