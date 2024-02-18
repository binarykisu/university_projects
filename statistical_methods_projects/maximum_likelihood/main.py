# Importing the necessary functions
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin
from scipy.optimize import minimize
from math import pi

def log_likelihood(x: list[float]) -> float:
    """Function defining the log-likelihood function.
    Returns: Negative log-likelihood : float"""
    
    # Defining constants and input arrays
    z = np.array([0, 6, 12, 18]) * 10**-6 # Heights where the clusters are observed
    n = np.array([1880, 940, 530, 305]) # Number of clusters observed for each height
    nu_0 = x[0] # Parameter to estimate number of clusters at z=0
    k = x[1] # Parameter to estimate Boltzmann constant
    r = 0.52 * 10**-6 # Radius of the clusters
    delta_rho = 1063 - 998 # Density difference between mastic and water
    g = 9.80 # Gravitational acceleration
    T = 293 # Absolute temperature in Kelvin
    
    # Calculates and returns the negative log-likelihood
    return -np.sum(n * (np.log(nu_0) - (4 * pi * r**3 * delta_rho * g * z) / (3 * k * T)) - nu_0 * np.exp((-4 * pi * r**3 * delta_rho * g * z) / (3 * k * T)))

# Defining initial values/guesses for the parameters
nu_0 = 1880 # Number of clusters observed at z=0
k = np.arange(1, 2.0005, 0.0005) * 10**-23 # Initial guesses for the Boltzmann constant
f = np.zeros(k.shape) # Will store the values of the negative log-likelihood function 
max_logL = -9999 # Initialized with a very large negative value
best_k = 9999  # Initialized with a very large positive value
best_i = 0 # Keeps track of the index corresponding to the best value of k

# Loop over k values to find the one that maximizes the log-likelihood
for i in range(len(k)):
    f[i] = -log_likelihood([nu_0, k[i]])
    if f[i] > max_logL:
        max_logL = f[i]
        best_k = k[i] # Best value for k is found in here
        best_i = i

# Calculates the uncertainty in k
uncertainty_m = k[np.where(f > (max_logL - 0.5))[0][0]]
uncertainty_p = k[np.where(f > (max_logL - 0.5))[0][-1]]

# Plotting the parameter estimation
plt.plot(k, f, '.', c="purple")
plt.title('Log likelihood parameter estimation')
plt.xlabel('Boltzmann constant, k [J/k]')
plt.ylabel('Log likelihood')
plt.show()

# Printing the results for part 1
print("\nPart 1:\n")
print(f"k: {best_k}")
print(f"Uncertainty of k: {(uncertainty_p - uncertainty_m) / 2}")

# Uses scipy's fmin function to find the minimum of the log-likelihood function
x, val = fmin(lambda x: log_likelihood(x), [nu_0, best_k], full_output=True)[:2]

# Defines a range of values for nu and k
theta_nu = np.arange(1800, 1890.01, 0.1)
theta_k = np.arange(1.15 * 10**-23, 1.35 * 10**-23, 0.01 * 10**-23)

# Initializes a matrix to store the log-likelihood for each combination of nu and k
likelihood_matrix = np.zeros((len(theta_nu), len(theta_k)))
for i in range(len(theta_nu)):
    for j in range(len(theta_k)):
        likelihood_matrix[i, j] = -log_likelihood([theta_nu[i], theta_k[j]])

# Determine which values of nu and k result in a log-likelihood within 0.5 of the max
uncertainty_matrix = likelihood_matrix >= (-val - 0.5)

# Plot the parameter estimation of k
plt.contour(theta_k, theta_nu, uncertainty_matrix)
plt.plot(x[1], x[0], '+')
plt.title('Parameter estimation with 1$\sigma$ confidence')
plt.xlabel('Boltzmann constant, k [J/k]')
plt.ylabel('nu_0')
plt.show()

# Prints the results for part 2
print("\nPart 2:\n")
print(f"k: {x[1]}")
print(f"nu_0: {x[0]}")
print(f"Uncertainty of k: {(np.where(np.sum(uncertainty_matrix, axis=0) > 0)[0][-1] - np.where(np.sum(uncertainty_matrix, axis=0) > 0)[0][0]) * 0.001 * 10**-23 / 2}")
print(f"Uncertainty of nu_0: {(np.where(np.sum(uncertainty_matrix, axis=1) > 0)[0][-1] - np.where(np.sum(uncertainty_matrix, axis=1) > 0)[0][0]) * 0.01 / 2}")

# Prints the results for part iii
# Calculates Avogadro's constant and its uncertainty
print("\nPart 3:\n")
print(f"Estimating Avogadro's constant: {8.314 / x[1]}")
print(f"Uncertainty of Avogadro's constant, N_A: {8.314 * (np.where(np.sum(uncertainty_matrix, axis=0) > 0)[0][-1] - np.where(np.sum(uncertainty_matrix, axis=0) > 0)[0][0]) * 0.001 * 10**-23 / 2 / (x[1]**2)}")
