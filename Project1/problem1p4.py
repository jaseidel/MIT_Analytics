#%%
import numpy as np 
import scipy.stats as spstats
import statsmodels.stats.multitest as sm

#Columns are sorted by class, with 0 for ALL and 1 for AML
golub_data = np.genfromtxt('./golub_data/golub.csv',delimiter=',')[1:,1:]
golub_classnames = np.genfromtxt('./golub_data/golub_cl.csv',delimiter=',')[1:,1:]

N_AML = np.sum(golub_classnames)
N_ALL = golub_classnames.shape[0] - N_AML
#Be sure data is sorted by class
ALL_data=golub_data[:,:27]
AML_data=golub_data[:,27:]

#%%
Xbar_ALL = np.mean(ALL_data, axis=1)
Xbar_AML = np.mean(AML_data, axis=1)

Var_ALL = np.var(ALL_data, ddof=1, axis=1)
Var_AML = np.var(AML_data, ddof=1, axis=1)


# %%
t_Welch = (Xbar_ALL - Xbar_AML) / np.sqrt(Var_ALL/N_ALL + Var_AML/N_AML)

v = np.power(Var_ALL/N_ALL + Var_AML/N_AML, 2) / (1/(N_ALL-1) * np.power(Var_ALL/N_ALL,2) + 1/(N_AML-1) * np.power(Var_AML/N_AML, 2))

p_vals1 = spstats.t.cdf(t_Welch,df=v)
count1 = p_vals1[np.where(p_vals1 < 0.025)].shape[0] + p_vals1[np.where(p_vals1 > 0.975)].shape[0]

# %%
t_stat, p_vals2 = spstats.ttest_ind(ALL_data, AML_data, axis=1, equal_var=False, alternative='two-sided')
count2 = p_vals2[np.where(p_vals2 < 0.05)].shape[0]


# %%

reject, p_val_corrected, alphacSidak, alphacBonf = sm.multipletests(p_vals2, alpha=0.05, method='holm', is_sorted=False)
print("Bonferroni-Holm:", np.sum(reject))

# %%
reject, p_val_corrected, alphacSidak, alphacBonf = sm.multipletests(p_vals2, alpha=0.05, method='fdr_bh', is_sorted=False)
print("Benjamini-Hochberg:", np.sum(reject))
# %%
