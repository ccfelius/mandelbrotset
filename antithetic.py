from mandelbrotset.monte import *
import scipy.stats as st
import math

def random_sampling(xmax=1.5,xmin=-2.5,ymax=1.5j,ymin=-1.5j, maxiter=100, samples = 1000, step = 0.01, antithetic=False):

    # calculate x range, y range and area
    xrange = xmax - xmin
    yrange = ymax - ymin
    area = xrange * (yrange * -1j).real

    in_mandelbrot = 0
    count = 0
    # for all samples, sample a random y and x value
    while count < samples:
        #note that ymin and ymax are complex numbers
        y_sample = random.uniform(ymin, ymax)
        x_sample = random.uniform(xmin, xmax)
        sample = x_sample + y_sample

        # check if in mandelbrotset
        if calculation(sample, maxiter, simulation = True):
            in_mandelbrot +=1

        if not antithetic:
            count += 1

        else:
            ay_sample = (ymin+ymax) - y_sample
            ax_sample = (xmin+xmax) - x_sample
            sample2 = ax_sample + ay_sample

            # check if in mandelbrotset
            if calculation(sample2, maxiter, simulation = True):
                in_mandelbrot +=1

            count += 2

        # calculate the estimated sample area
    sample_area = in_mandelbrot / samples * area

    return sample_area

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

# Orthogonal sampling works optimal if root of amount
# of samples is int
samples = 3600
simulations = 100
p_value = 0.95
maxiter = 200

EX = mandelbrot(xmax, xmin, ymax, ymin, maxiter) # gives 1.5139

# Simulations
rs_samples = []
rs_samples_a = []
lhs_samples = []
orth_samples = []

for n in range(1, simulations+1):
    r_sampling = random_sampling(xmax, xmin, ymax, ymin, maxiter, samples)
    r_sampling_a = random_sampling(xmax, xmin, ymax, ymin, maxiter, samples, antithetic=True)
    lhs_sim = LHS(xmax, xmin, ymax, ymin, maxiter, samples, plot=False)
    orth_sim = orthogonal_sampling(xmax, xmin, ymax, ymin, maxiter, samples, plot=False)
    print(f"Simulation {n}, s={samples}, i={maxiter}, RS: {r_sampling}, RSA: {r_sampling_a}, LHS: {lhs_sim}, Orthogonal: {orth_sim}")
    rs_samples.append(r_sampling)
    rs_samples_a.append(r_sampling_a)
    lhs_samples.append(lhs_sim)
    orth_samples.append(orth_sim)


print(f"\nEstimated Mandelbrot Area {EX}")
print(f"Simulations: {simulations}, Samples: {samples}\nVariance RS: {np.var(rs_samples)}, antithetic: {np.var(rs_samples_a)}\nVariance LHS: {np.var(lhs_samples)}\nVariance Orthogonal Sampling: {np.var(orth_samples)}\n ")
print(f"Estimated Mandelbrot Area E[X]: {EX:.4f}")
print(conf_int(np.mean(rs_samples), np.var(rs_samples), simulations, p=0.95))
print(conf_int(np.mean(rs_samples_a), np.var(rs_samples_a), simulations, p=0.95))
print(conf_int(np.mean(lhs_samples), np.var(lhs_samples), simulations, p=0.95))
print(conf_int(np.mean(orth_samples), np.var(orth_samples), simulations, p=0.95))
print(np.mean(rs_samples))
print(np.mean(rs_samples_a))
print(np.mean(lhs_samples))
print(np.mean(orth_samples))

print(np.std(rs_samples))
print(np.std(rs_samples_a))
print(np.std(lhs_samples))
print(np.std(orth_samples))

