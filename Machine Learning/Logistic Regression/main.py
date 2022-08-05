#!/usr/bin/env python
# coding: utf-8

# In[232]:


import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import random


# Data Preparation

# In[370]:


data = pd.read_csv("vehicle.csv")             
xa = data.loc[data['Class'] == 'saab', 'COMPACTNESS':'Class']      
xb = data.loc[data['Class'] == 'van', 'COMPACTNESS':'Class']
x_concat = pd.concat([xa, xb])          
x_shuffled = x_concat.sample(frac = 1)  
x_with_class = x_shuffled


# In[371]:


N = len(x_with_class)     
nof_features = len(x_with_class.columns) -1  
y = np.ones(N)
#converts class labels into -1 and 1
for i in range (N):
    if(x_with_class.iloc[i]['Class'] == 'saab'):
        y[i] = -1
x = (x_with_class.iloc[:,:-1]).to_numpy()

fold_size = np.int(np.floor(N/5))
f1 = x[:fold_size]
f2 = x[fold_size: 2*fold_size]
f3 = x[2*fold_size: 3*fold_size]
f4 = x[3*fold_size: 4*fold_size]
f5 = x[4*fold_size:]
l1 = y[:fold_size]
l2 = y[fold_size: 2*fold_size]
l3 = y[2*fold_size: 3*fold_size]
l4 = y[3*fold_size: 4*fold_size]
l5 = y[4*fold_size:]
x1_train = np.concatenate((f1, f2, f3, f4), axis=0)
x2_train = np.concatenate((f1, f2, f3, f5), axis=0)
x3_train = np.concatenate((f1, f2, f4, f5), axis=0)
x4_train = np.concatenate((f1, f3, f4, f5), axis=0)
x5_train = np.concatenate((f2, f3, f4, f5), axis=0)
x1_test = f5
x2_test = f4
x3_test = f3
x4_test = f2
x5_test = f1
y1_train = np.concatenate((l1, l2, l3, l4), axis=0)
y2_train = np.concatenate((l1, l2, l3, l5), axis=0)
y3_train = np.concatenate((l1, l2, l4, l5), axis=0)
y4_train = np.concatenate((l1, l3, l4, l5), axis=0)
y5_train = np.concatenate((l2, l3, l4, l5), axis=0)
y1_test = l5
y2_test = l4
y3_test = l3
y4_test = l2
y5_test = l1


# ## Step 1

# In[372]:


if((sys.argv[1] == 'part1') and (sys.argv[2] == 'step1')) :

    #sigmoid function
    def sigmoid(s):
        return (1 / (1+ math.exp(-s)))

    #calculates average error of given data set
    def E(w, x, y):
        N = len(x)
        sum = 0
        for i in range(N):
            sum += np.log(1 + math.exp(-y[i]* np.dot(w.T, x[i])))
        return (sum/N)

    #logistic loss function
    def gradient(w, x, y):
        N = len(x)
        sum = 0
        for i in range(N):
            sum += -y[i]*x[i]* sigmoid(-y[i]* np.dot(w.T, x[i]))
        return (sum/N)


    def gradient_descent(x, y):
        N = len(x)
        w = np.zeros(nof_features)
        n = 0.001
        error = []
        for i in range(5000):
            e = E(w, x, y)
            g = gradient(w, x, y)
            error.append(e)
            v = -g  / (np.linalg.norm(g))
            w = w + n*v
        plt.plot(error)
        return w 

    w1 = gradient_descent(x5_train, y5_train)
    e1 = E(w5, x5_test, y5_test)
    w2 = gradient_descent(x2_train, y2_train)
    e2 = E(w2, x2_test, y2_test)
    w3 = gradient_descent(x3_train, y3_train)
    e3 = E(w3, x3_test, y3_test)
    w4 = gradient_descent(x4_train, y4_train)
    e4 = E(w4, x4_test, y4_test)
    w5 = gradient_descent(x5_train, y5_train)
    e5 = E(w5, x5_test, y5_test)
    print("Error is: " + str((e1+e2+e3+e4+e5)/5))


# ## Step 2

# In[394]:


if((sys.argv[1] == 'part1') and (sys.argv[2] == 'step2')) :
    def stochastic_gradient_descent(x, y):
        N = len(x)
        w = np.zeros(nof_features)
        n = 0.000001
        error = []
        for i in range(30000):
            r = random.randint(0, N-1)
            e = E(w, x, y)
            error.append(e)
            w += x[r]*y[r]*(n/(1+ math.exp(y[r]*np.dot(w.T, x[r]))))
        plt.plot(error)
        return w 

    w1 = stochastic_gradient_descent(x5_train, y5_train)
    e1 = E(w5, x5_test, y5_test)
    w2 = stochastic_gradient_descent(x2_train, y2_train)
    e2 = E(w2, x2_test, y2_test)
    w3 = stochastic_gradient_descent(x3_train, y3_train)
    e3 = E(w3, x3_test, y3_test)
    w4 = stochastic_gradient_descent(x4_train, y4_train)
    e4 = E(w4, x4_test, y4_test)
    w5 = stochastic_gradient_descent(x5_train, y5_train)
    e5 = E(w5, x5_test, y5_test)

    print("Error is: " + str((e1+e2+e3+e4+e5)/5))
