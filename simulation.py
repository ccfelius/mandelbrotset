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


## Simulations
z = 0.0j
step = 0.01
xmax= 0.5
xmin= -2.0
ymax= 1.1j
ymin= -1.1j

# Orthogonal sampling works optimal if root of amount of samples is int
samples = 3600
simulations = 100
p_value = 0.95
maxiter = 1900

# calculate area of mandelbrot brute-force
EX = mandelbrot(xmax, xmin, ymax, ymin, maxiter)

# # Simulations
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
# #
#
print(f"\nEstimated Mandelbrot Area {EX}")
print(f"Simulations: {simulations}, Samples: {samples}\nVariance RS: {np.var(rs_samples)}\nVariance LHS: {np.var(lhs_samples)}\nVariance Orthogonal Sampling: {np.var(orth_samples)}\n ")
print(f"Simulations: {simulations}, Samples: {samples}\nSTD RS: {np.std(rs_samples)}\nSTD LHS: {np.std(lhs_samples)}\nSTD Orthogonal Sampling: {np.std(orth_samples)}\n ")
print(f"Estimated Mandelbrot Area E[X]: {EX:.4f}")
print(conf_int(np.mean(rs_samples), np.var(rs_samples), simulations, p=0.95))
print(conf_int(np.mean(lhs_samples), np.var(lhs_samples), simulations, p=0.95))
print(conf_int(np.mean(orth_samples), np.var(orth_samples), simulations, p=0.95))
print(np.mean(rs_samples))
print(np.mean(lhs_samples))
print(np.mean(orth_samples))


