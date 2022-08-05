import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

### Step 1
# 50 points in two classes

# In[67]:


if((sys.argv[1] == 'part1') and (sys.argv[2] == 'step1')) :
    X = np.zeros(shape=(50,3))
    X0 = np.ones(shape=(50,1))
    X[:,0] = X0[:,0]
    a = np.random.randint(-100,100, size=50)
    b = np.random.randint(-300,300, size=50)
    t = np.zeros(50)
    for i in range(50):
        if(-3*a[i]+1<b[i]):
            t[i] = 1
        else:
            t[i] = 0
    X[:,1] = a
    X[:,2] = b
    W = np.array([ 0, 0, 0])
    for i in range(10000):
        for j in range(50):
            if(np.sign(np.dot(W, X[j])) != t[j]):
                if(np.sign(np.dot(W, X[j])) == 1):
                    W = W + np.dot([-1, -1, -1], X[j])*0.01
                else:
                    W = W + np.dot(t[j], X[j])*0.01

    print(f"Weight vector is: {W}")

    plt.plot(X[:,1][t==0], X[:,2][t==0], 'o', color='red',markersize=1.5);
    plt.plot(X[:,1][t==1], X[:,2][t==1], 'o', color='blue',markersize=1.5);
    x = np.arange(-100, 100, 2)
    plt.plot(x, -W[0]/W[2] - W[1]*x/W[2], color='purple', label = 'Decision Boundary' )
    plt.plot(x, -3*x+1, color='green', label = 'Target Separating Function f' )
    plt.title("Seperating 50 Data Points")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()


### Step 2
# 100 points in two classes
# In[13]:


if((sys.argv[1] == 'part1')and (sys.argv[2] == 'step2')) :
    X = np.zeros(shape=(100,3))
    X0 = np.ones(shape=(100,1))
    X[:,0] = X0[:,0]
    a = np.random.randint(-100,100, size=100)
    b = np.random.randint(-300,300, size=100)
    t = np.zeros(100)
    for i in range(100):
        if(-3*a[i]+1<b[i]):
            t[i] = 1
        else:
            t[i] = 0
    X[:,1] = a
    X[:,2] = b
    W = np.array([0,0,0])

    for i in range(1000):
        for j in range(100):
            if(np.sign(np.dot(W, X[j])) != t[j]):
                if(np.sign(np.dot(W, X[j])) == 1):
                    W = W + np.dot([-1, -1, -1], X[j])*0.01
                else:
                    W = W + np.dot(t[j], X[j])*0.01
                    
    print(f"Weight vector is: {W}")

    plt.plot(X[:,1][t==0], X[:,2][t==0], 'o', color='red',markersize=1.5);
    plt.plot(X[:,1][t==1], X[:,2][t==1], 'o', color='blue',markersize=1.5);
    x = np.arange(-100, 100, 2)
    plt.plot(x, -W[0]/W[2] - W[1]*x/W[2], color='purple', label = 'Decision Boundary' )
    plt.plot(x, -3*x+1, color='green', label = 'Target Separating Function f' )
    plt.title("Seperating 100 Data Points")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()


### Step 3
# 5000 points in two classes
# In[10]:


if((sys.argv[1] == 'part1')and (sys.argv[2] == 'step3')) :
    X = np.zeros(shape=(5000,3))
    X0 = np.ones(shape=(5000,1))
    X[:,0] = X0[:,0]
    a = np.random.randint(-100,100, size=5000)
    b = np.random.randint(-300,300, size=5000)
    t = np.zeros(5000)
    for i in range(5000):
        if(-3*a[i]+1<b[i]):
            t[i] = 1
        else:
            t[i] = 0
    X[:,1] = a
    X[:,2] = b
    W = np.array([0,0,0])
    for i in range(200):
        for j in range(5000):
            if(np.sign(np.dot(W, X[j])) != t[j]):
                if(np.sign(np.dot(W, X[j])) == 1):
                    W = W + np.dot([-1, -1, -1], X[j])*0.01
                else:
                    W = W + np.dot(t[j], X[j])*0.01
    
    print(f"Weight vector is: {W}")

    plt.plot(X[:,1][t==0], X[:,2][t==0], 'o', color='red',markersize=1);
    plt.plot(X[:,1][t==1], X[:,2][t==1], 'o', color='blue',markersize=1);
    x = np.arange(-100, 100, 2)
    plt.plot(x, -W[0]/W[2] - W[1]*x/W[2], color='purple', label = 'Decision Boundary' )
    plt.plot(x, -3*x+1, color='green', label = 'Target Separating Function f' )
    plt.title("Seperating 5000 Data Points")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()
