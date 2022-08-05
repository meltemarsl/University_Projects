import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# In[73]:


df = pd.read_csv(r"C:\Users\Meltem Arslan\Desktop\part2_datasets\ds1.csv", header=None)
nof_columns = len(df.columns)
N = len(df)
shuffled_df = df.sample(frac = 1)
x_train = shuffled_df.loc[:, :nof_columns-2]
y_train = shuffled_df.loc[:, nof_columns-1:]

ones = np.ones([N,1])
x_train = np.concatenate((ones, x_train), axis=1)


# In[74]:


if((sys.argv[1] == 'part2')and (sys.argv[2] == 'step1') ) :
    a = datetime.datetime.now()
    w = np.dot(np.dot(np.linalg.inv(np.dot(x_train.T, x_train)), x_train.T), y_train)
    b = datetime.datetime.now()
    delta = b - a
    time = str(int(delta.total_seconds() * 1000)) # milliseconds
    print("Time to complete step1: "+ time +" msec")


# In[75]:


df = pd.read_csv(r"C:\Users\Meltem Arslan\Desktop\part2_datasets\ds2.csv", header=None)
nof_columns = len(df.columns)
N = len(df)
shuffled_df = df.sample(frac = 1)
x_train = shuffled_df.loc[:, :nof_columns-2]
y_train = shuffled_df.loc[:, nof_columns-1:]

ones = np.ones([N,1])
x_train = np.concatenate((ones, x_train), axis=1)


# In[84]:


if((sys.argv[1] == 'part2')and (sys.argv[2] == 'step2') ) :
    a = datetime.datetime.now()
    w = np.dot(np.dot(np.linalg.inv(np.dot(x_train.T, x_train)), x_train.T), y_train)
    b = datetime.datetime.now()
    delta = b - a
    time = str(int(delta.total_seconds() * 1000)) # milliseconds
    print("Time to complete step2: "+ time +" msec")


# In[86]:


if((sys.argv[1] == 'part2')and (sys.argv[2] == 'step3')) :
    lmd = 500
    I = np.identity(nof_columns)
    a = datetime.datetime.now()
    wR = np.dot(np.dot(np.linalg.inv(np.dot(x_train.T, x_train) + lmd*I ), x_train.T), y_train)
    b = datetime.datetime.now()
    delta = b - a
    time = str(int(delta.total_seconds() * 1000)) # milliseconds
    print("Time to complete step3: "+ time +" msec")
