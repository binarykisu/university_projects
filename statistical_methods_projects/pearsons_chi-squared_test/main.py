# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2, poisson
from pathlib import Path

# Load the path of text files
real_mass_path = Path(__file__).with_name('real_mass.txt')
mc1_mass_path = Path(__file__).with_name('MC1_mass.txt')
mc2_mass_path = Path(__file__).with_name('MC2_mass.txt')

# Load the information from the files
real_mass = np.loadtxt(real_mass_path)
mc1_mass = np.loadtxt(mc1_mass_path)
mc2_mass = np.loadtxt(mc2_mass_path)

# Calculate chi-square values for MC1 and MC2
# Chi-square is a statistical test that tells how observations are distributed across different outcomes
chi2_1 = np.sum((real_mass[:, 2] - mc1_mass[:, 2]) ** 2 / mc1_mass[:, 2]) # For background 1
chi2_2 = np.sum((real_mass[:, 2] - mc2_mass[:, 2]) ** 2 / mc2_mass[:, 2]) # For background 2
print(f"\nThe chi^2 values for MC1 and MC2 are {chi2_1:.2f} and {chi2_2:.2f}, respectively.")

# Calculate P-values using chi-square cumulative distribution
# P-value is the probability that, if the null hypothesis were true, we would observe a more extreme test statistic
dof = len(real_mass[:, 2]) # Degrees of freedom
P_1 = 1 - chi2.cdf(chi2_1, dof) # P-value for background 1
P_2 = 1 - chi2.cdf(chi2_2, dof) # P-value for background 2
print(f"\nThe P-values for backgrounds 1 and 2 are P1 = {P_1:.0f} and P2 = {P_2:.3f}.")

# **Perform pseudoexperiments by generating simulated data based on the Poisson distribution 
# with means given by the simulated mass data for backgrounds 1 and 2**

edges = np.append(real_mass[:, 0], np.max(real_mass[:, 1])) # Defines edges of histogram bins
k = 10000 # Number of data samples

pseudo_1 = np.zeros((len(mc1_mass[:, 2]), k)) 
pseudo_2 = np.zeros((len(mc2_mass[:, 2]), k))

for i in range(len(mc1_mass[:, 2])):
    pseudo_1[i, :] = poisson.rvs(mc1_mass[i, 2], size=k) # For background 1

for i in range(len(mc2_mass[:, 2])):
    pseudo_2[i, :] = poisson.rvs(mc2_mass[i, 2], size=k) # For background 2

# Chi-square values are calculated for the pseudoexperiments
chi2_1_pseudo = np.zeros(k)
chi2_2_pseudo = np.zeros(k)

for i in range(k):
    chi2_1_pseudo[i] = np.sum((pseudo_1[:, i] - mc1_mass[:, 2]) ** 2 / mc1_mass[:, 2]) # For background 1
    chi2_2_pseudo[i] = np.sum((pseudo_2[:, i] - mc2_mass[:, 2]) ** 2 / mc2_mass[:, 2]) # For background 2
    
# Calculate P-values using pseudoexperiments
P_1_pseudo = np.sum(chi2_1_pseudo > chi2_1) / k
P_2_pseudo = np.sum(chi2_2_pseudo > chi2_2) / k

print(f"\nThe P-values for pseudoexperiments with backgrounds 1 and 2 are P1 = {P_1_pseudo:.3f} and P2 = {P_2_pseudo:.3f}.")

# Plotting the chi-square distributions with histograms
chi2_values = np.arange(0, 101, 1) # x-axis values 1-100
chi2_hist_p1, _ = np.histogram(chi2_1_pseudo, bins=chi2_values, density=True) # y-axis values
chi2_hist_p2, _ = np.histogram(chi2_2_pseudo, bins=chi2_values, density=True) # y-axis values

# Plotting the first figure against backgrounds 1 and 2
plt.plot(chi2_values, chi2.pdf(chi2_values, dof), 'g', label='Theoretical')
plt.plot(chi2_values[:100], chi2_hist_p1, 'r', label='Pseudo - Bkg 1')
plt.plot(chi2_values[:100], chi2_hist_p2, 'b', label='Pseudo - Bkg 2')
plt.legend()
plt.xlabel('$\chi^{2}$ values')
plt.ylabel('Probability')
plt.title('Real data vs. Backgrounds 1 & 2')
plt.show()

# Find optimal value of parameter 'a' 
best_a = 0 # Should best combine the backgrounds 1 and 2 to model the real data
chi2_min = np.inf # Minimum chi-square value obtained during the search for best_a

for a in np.arange(0, 1.0001, 0.0001):
    combo = a * mc1_mass + (1 - a) * mc2_mass
    chi2_combo = np.sum((real_mass[:, 2] - combo[:, 2]) ** 2 / combo[:, 2])
    if chi2_combo < chi2_min:
        chi2_min = chi2_combo
        best_a = a # Found best 'a'

best_combo = best_a * mc1_mass + (1 - best_a) * mc2_mass # Combination of backgrounds 1 and 2 that best models the real data based on 'a'
P_theor = 1 - chi2.cdf(chi2_min, dof) # Theoretical p-value calculated using the minchi2 value

# Doing the same thing but for pseudoexperimental data
pseudo_combo = np.zeros((len(mc1_mass[:, 2]), k))
for i in range(len(mc1_mass[:, 2])):
    pseudo_combo[i, :] = poisson.rvs(best_combo[i, 2], size=k)

chi2_combo = np.zeros(k)
for i in range(k):
    chi2_combo[i] = np.sum((pseudo_combo[:, i] - best_combo[:, 2]) ** 2 / best_combo[:, 2])

P_combo = np.sum(chi2_combo > chi2_min) / k

print(f"\nCombining backgrounds 1 and 2 to best model the real data:")
print(f"Value of 'a' that best combines the backgrounds: a = {best_a:.3f}")
print(f"Minimum chi-square value obtained while finding 'a': {chi2_min:.2f}")
print(f"P-value based on the chi-square value: P = {P_theor:.3f}")
print(f"P-value for pseudoexperiments: P = {P_combo:.3f}\n")


# Plotting the second figure with the combined background
plt.plot(best_combo[:, 0], best_combo[:, 2], '-b', label='Combination of bkg')
plt.plot(real_mass[:, 0], real_mass[:, 2], '-g', label='Data')
plt.legend()
plt.xlabel('Mass')
plt.ylabel('Probability')
plt.title('Real data vs. Optimal/Combined background')
plt.show()
