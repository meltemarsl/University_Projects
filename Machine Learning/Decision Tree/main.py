#!/usr/bin/env python
# coding: utf-8

# In[29]:


import sys
import numpy as np
import pandas as pd
from libsvm.svmutil import *

# Data Preparation

# In[30]:


data = pd.read_csv("iris.csv")
header = []
for col in data.columns:
    header.append(col)
xs_train = data.loc[0:39, data.columns != 'class']
xs_test = data.loc[40:49, data.columns != 'class']
xv_train = data.loc[50:89, data.columns != 'class']
xv_test = data.loc[90:99, data.columns != 'class']
x_train0 = pd.concat([xs_train, xv_train])
x_test0 = pd.concat([xs_test, xv_test])
x_train = (x_train0).to_numpy()
x_test = (x_test0).to_numpy()

ys_train = np.ones([40])
ys_test = np.ones([10])
yv_train = np.zeros([40])
yv_test = np.zeros([10])
y_train = np.concatenate((ys_train, yv_train), axis=0)
y_test = np.concatenate((ys_test, yv_test), axis=0)


# In[31]:


def entropy(p, n):
    if((n == 0) or (p == 0)):
        return 0
    entropy = -(p/(p+n))*np.log2(p/(p+n)) - (n/(p+n))*np.log2(n/(p+n))
    return entropy


# In[32]:


class Node:
    def __init__(self, depth, x, y):
        self.left = None
        self.right = None
        self.attribute = None
        self.threshold = None
        self.x = x
        self.y = y
        self.depth = depth


# In[33]:


class Tree:
    def __init__(self, x_train, y_train):
        self.root = Node(depth = 0, x = x_train, y = y_train)


# In[34]:


def isLeaf(node):
    if(node.depth == 6):
        return True
    elif(0 not in node.y):
        return True
    elif(1 not in node.y):
        return True
    else:
        return False


# In[35]:


def split(node):
    if(isLeaf(node) == False):
        threshold, attribute = findAttribute(node)
        node.attribute = attribute
        node.threshold = threshold
        lx = []
        ly = []
        rx = []
        ry = []
        for i in range(len(node.x)):
            if(threshold >= node.x[i][attribute]):
                lx.append(node.x[i])
                ly.append(node.y[i])
            else:
                rx.append(node.x[i])
                ry.append(node.y[i])
        node.left = Node(node.depth+1, lx, ly)
        node.right = Node(node.depth+1, rx, ry)
        split(node.left)
        split(node.right)


# In[36]:


def traverse(tree, x_test):
    node = tree.root
    while(isLeaf(node) == False):
        if(node.threshold >= x_test[node.attribute]):
            node = node.left
        else:
            node = node.right
    if((0 not in node.y) or (1 not in node.y)):
        prediction = node.y[0]
    else:
        if(np.sum(y) < len(y)/2):
            prediction = 0
        else:
            prediction = 1
    return prediction


# ## Step 1

# In[41]:


if((sys.argv[1] == 'part1') and (sys.argv[2] == 'step1')) :
    def findAttribute(node):
        threshold = np.zeros([4])
        IG = np.zeros([4])
        s = 0
        v = 0
        for t in range(len(node.y)):
            if(node.y[t] == 1):
                s+=1
            else:
                v+=1
        node_entropy = entropy(s, v)
        for f in range(4):
            for i in range(len(node.x)):
                threshold_i = node.x[i][f]

                s_below = 0
                v_below = 0
                s_above = 0
                v_above = 0
                for k in range(len(node.x)):
                    if((threshold_i >= node.x[k][f]) and (node.y[k] == 1)):
                        s_below +=1
                    elif((threshold_i >= node.x[k][f]) and (node.y[k] == 0)):
                        v_below +=1
                    elif((threshold_i < node.x[k][f]) and (node.y[k] == 1)):
                        s_above +=1
                    elif((threshold_i < node.x[k][f]) and (node.y[k] == 0)):
                        v_above +=1
                if(s_above+ v_above == 0):
                    IG_i = node_entropy - entropy(s_below, v_below)
                elif(s_below+ v_below == 0):
                    IG_i = node_entropy - entropy(s_above, v_above)
                else:
                    IG_i = node_entropy - (((s_above+ v_above) / 80) * entropy(s_above, v_above) + ((s_below+ v_below) / 80) * entropy(s_below, v_below))
                if(IG_i > IG[f]):
                    IG[f] = IG_i
                    threshold[f] = threshold_i
        return threshold[np.argmax(IG)], np.argmax(IG)

    tree = Tree(x_train, y_train)
    split(tree.root)
    predict = []
    for i in range(len(x_test)):
        predict.append(traverse(tree, x_test[i]))
    count =0
    for i in range(len(x_test)):
        if(y_test[i] == predict[i]):
            count+=1

    accuracy = count/len(predict)
    print("DT " + str(header[tree.root.attribute]) + " " + str(accuracy))


# ## Step 2

# In[42]:


if((sys.argv[1] == 'part1') and (sys.argv[2] == 'step2')) :
    def findAttribute(node):
        threshold = np.zeros([4])
        GR = np.zeros([4])
        s = 0
        v = 0
        for t in range(len(node.y)):
            if(node.y[t] == 1):
                s+=1
            else:
                v+=1
        node_entropy = entropy(s, v)
        for f in range(4):
            for i in range(len(node.x)):
                threshold_i = node.x[i][f]

                s_below = 0
                v_below = 0
                s_above = 0
                v_above = 0
                for k in range(len(node.x)):
                    if((threshold_i >= node.x[k][f]) and (node.y[k] == 1)):
                        s_below +=1
                    elif((threshold_i >= node.x[k][f]) and (node.y[k] == 0)):
                        v_below +=1
                    elif((threshold_i < node.x[k][f]) and (node.y[k] == 1)):
                        s_above +=1
                    elif((threshold_i < node.x[k][f]) and (node.y[k] == 0)):
                        v_above +=1
                total = s_above + v_above + s_below + v_below
                if(s_above+ v_above == 0):
                    IG_i = node_entropy - entropy(s_below, v_below)
                    GR_i = IG_i /((s_below+ v_below) / total) 
                elif(s_below+ v_below == 0):
                    IG_i = node_entropy - entropy(s_above, v_above)
                    GR_i = IG_i /((s_above+ v_above) / total)
                else:
                    IG_i = node_entropy - (((s_above+ v_above) / total) * entropy(s_above, v_above) + ((s_below+ v_below) / total) * entropy(s_below, v_below))
                    GR_i = IG_i / -(((s_above+ v_above) / total) *np.log2((s_above+ v_above) / total) + ((s_below+ v_below) / total) *np.log2((s_below+ v_below) / total))
                if(GR_i > GR[f]):
                    GR[f] = GR_i
                    threshold[f] = threshold_i
        return threshold[np.argmax(GR)], np.argmax(GR)

    tree = Tree(x_train, y_train)
    split(tree.root)
    predict = []
    for i in range(len(x_test)):
        predict.append(traverse(tree, x_test[i]))
    #print(len(predict))
    count =0
    for i in range(len(x_test)):
        if(y_test[i] == predict[i]):
            count+=1

    accuracy = count/len(predict)
    print("DT " + str(header[tree.root.attribute]) + " " + str(accuracy))
