#%%
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import csv
%matplotlib inline

#%%
X = np.genfromtxt('syn_X.csv',delimiter=',')
X = np.column_stack((np.ones(X.shape[0]),X))
y = np.genfromtxt('syn_y.csv',delimiter=',')

#%%
#mortality_df = pd.read_csv("mortality.csv", header=0, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)

# %%
def  loss(theta,X,y):
    loss = (y - X @ theta).T @ (y- X @ theta)
    print("loss:", loss)
    return

def grad(theta,X,y):
    grad = (-2 * ( y.T @ X + 2 * theta.T @ X.T @ X))
    print("grad:",grad)
    return grad

    

def grad_desc(X,y,theta,alpha,iter=100):
    m = len(y)
    loss_history = np.zeros(iter)
    
    for i in range(iter):
        print("theta:", theta)
        loss_history[i] = loss(theta,X,y)
        theta = theta - alpha * grad(theta,X,y) 
        if  loss_history[i] <= 10**(-6):
            print("converged:", i)
            return theta, loss_history #, theta_history
            #, cost_history, theta_history
    return theta, loss_history #, theta_history

#%%
theta = np.random.randn(3)
alpha = .0005
iter = 100


theta, loss_history = grad_desc(X,y,theta,alpha,iter)

#print(theta)

fig,ax = plt.subplots(figsize=(12,8))

ax.set_ylabel('J(Theta)')
ax.set_xlabel('Iterations')
_=ax.plot(range(iter),loss_history,'b.')


# %%
