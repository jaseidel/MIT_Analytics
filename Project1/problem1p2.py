#%%
import numpy as np 
import scipy.stats 
data = np.genfromtxt('gamma-ray.csv',delimiter=',')[1:]

#%%

column_sums = np.sum(data, axis=0)
counts_sum = column_sums[1]
seconds_sum = column_sums[0]
tot_average_rate = counts_sum / seconds_sum

seconds_col = data[:,0]
counts_sample_col = data[:,1]

counts_expect_col = seconds_col * tot_average_rate


#%%
H0_likelihood = np.product(scipy.stats.poisson.pmf(counts_sample_col, counts_expect_col))
HA_likelihood = np.product(scipy.stats.poisson.pmf(counts_sample_col, counts_sample_col))

print(H0_likelihood)
print(HA_likelihood)

#%%
LR = (H0_likelihood / HA_likelihood)
lam = -2* np.log(LR)
p_value = 1-scipy.stats.chi2.cdf(lam,99)



# %%
