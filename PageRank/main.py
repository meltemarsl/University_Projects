#!/usr/bin/env python
# coding: utf-8

# In[14]:


#teleporting rate
tr = 0.15


# In[21]:


#file reading
f = open("data.txt", "r")      
data = f.readline()
nodes = data.split()[1]
nodes = int(nodes)


# In[22]:


indexes = {}   # to hold the names of the indexes
linkForward = {}   # holds the nodes that can be reachable from the current node as a set


# In[23]:


nl = sum(1 for line in open('data.txt'))
for i in range(1, nodes+1):
    data = f.readline()
    beginEnd = [i for i in range(len(data)) if data.startswith("\"", i)]  # gets the names of the nodes
    indexes[i] = data[beginEnd[0]+1:beginEnd[1]]
data = f.readline()
for i in range(nodes+3,nl+1):
    data = f.readline()
    data = data.split()   # data list holds to nodes that have edges between them
    try:
        s1 = linkForward[data[0]]  
    except:
        s1 = set()
    try: 
        s2 = linkForward[data[1]]
    except:
        s2 = set()
    
    s1.add(data[1])
    s2.add(data[0])
    linkForward[data[0]] = s1   #renew the nodes that can be reachable from the first element of the line
    linkForward[data[1]] = s2   #renew the nodes that can be reachable from the second element of the line


# In[24]:


probMatrix = [[0 for i in range(nodes)] for j in range(nodes)]          # 459 = number of rows/columns
for y in range(nodes):
    for x in range(nodes):
        try:
            s = linkForward[str(y+1)]
        except:
            s = set()
        if(str(x+1) in s):  # the node x+1 is  reachable from y+1
            probMatrix[y][x] = (tr/nodes) + ((1-tr)/len(s))   
        else:
            probMatrix[y][x] = (tr/nodes)


# In[25]:


x = []   #a list to hold current probabilities
for i  in range(nodes):
    x.append(1/nodes)
x_prev = [] #a list to hold previous probabilities
summ=5
while(summ > 1e-10):  # if the sum of the elementwise differences is greater them 1e-10, the list is not stable
    x_prev = x
    x = []
    for to in range(nodes):  # iterates through the rows of the matrix
        value = 0  # value will hold the sum of probabilities to reach the current node "to"
        for fromm in range(nodes):
            value += x_prev[fromm]*probMatrix[fromm][to]  # add (the probability to be in the node "fromm" * the probability to reach "to" from "fromm"
        x.append(value)
    summ = 0 
    for i in range(nodes):
        summ += abs(x[i] - x_prev[i])    # sum holds the sum of differences between to list


# In[26]:


orderdict = {}    # to hold the indexes as well as pagerank values
for i in range(nodes):
    orderdict[i] = x[i]
sorted_x = {k: v for k, v in sorted(orderdict.items(),reverse=True, key=lambda item: item[1])}  #sorts the dict according to pagerank values in decreasing order


# In[27]:



# prints the names of the top 50 and their pagerank scores
n = 0
for key in sorted_x:
    if(n<50):
        print(indexes[key+1], '->', sorted_x[key])
        n+=1


# In[ ]:




