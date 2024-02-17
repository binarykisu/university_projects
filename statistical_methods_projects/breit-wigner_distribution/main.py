import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Initialize arrays
sample_size = 10000
r = np.zeros(sample_size)
E = np.zeros(sample_size)

start = 0
end = 50
step = 0.1
x = np.arange(start, end, step)  # generating values for x

E_s = 25  # mean energy of an unstable state
gamma_s = 5  # uncertainty on the mean energy, E_s

# Generate random numbers and calculate the energy E
for i in range(sample_size):
    r[i] = np.random.randn()  # r values will be uniformly distributed random numbers betweeen 0 and 1
    E[i] = (gamma_s / 2) * np.tan(np.pi * (r[i] - 0.5)) + E_s  # this is a function E(r) which gives the probability distribution function

# Histogram calculation
a, _ = np.histogram(E, bins=np.arange(start, end + step, step))

# Fitting x and y data to a Gaussian curve
E_fitted = x[(x >= 21) & (x <= 29)]
y_fitted = a[(x >= 21) & (x <= 29)]  
y_fitted = (y_fitted - np.min(y_fitted)) / (np.max(y_fitted) - np.min(y_fitted)) / 0.08 # normalizing y_fitted

# Define Gaussian distribution function
def gaussian(x, mu, sigma):
    return 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) * np.sum(y_fitted)

# Want to minimize the loss (negative log-likelihood) to find optimal values for mu and sigma
def loss(params, x, y):
    mu, sigma = params
    if sigma == 0:
        return float('inf') # avoiding a divide-by-zero error
    else:
        y_pred = gaussian(x, mu, sigma) # predicted values
        return -np.sum(np.log1p(y_pred) * y)

# Initial guesses for the parameters
initial_guess = [25, 1]

# Perform optimization with the minimization function
optim_result = minimize(loss, initial_guess, args=(E_fitted, y_fitted))

# Extract the optimal mu and sigma parameters
mu_opt, sigma_opt = optim_result.x
#print(mu_opt, sigma_opt) # If you want to know the values for mu and sigma optimized

# Plot the histogram of the data
plt.figure(figsize=(12, 6))
plt.bar(x, a, width=0.1)

# Plot fitted Gaussian curve
plt.plot(x, gaussian(x, mu_opt, sigma_opt), label='Gaussian fitted curve', c="r")
plt.legend()
plt.xlabel('E')
plt.ylabel('dN/dE')

plt.title('Breit-Wigner distribution')
plt.show() # Displays the figures together
