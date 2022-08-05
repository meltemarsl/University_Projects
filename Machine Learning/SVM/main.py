# In[12]:


data = pd.read_csv("wbcd.csv")

train0 = data.loc[0:399, data.columns !=  'id']
test0 = data.loc[400:568, data.columns != 'id']
train = (train0).to_numpy()
test = (test0).to_numpy()
x_train = train[:,1:31]
x_test = test[:,1:31]
y_train = train[:, 0:1]
y_test = test[:, 0:1]
for i in range(400):
    if(y_train[i] == 'B'):
        y_train[i] = 0
    else:
        y_train[i] = 1
for i in range(169):
    if(y_test[i] == 'B'):
        y_test[i] = 0
    else:
        y_test[i] = 1


# ## Step 1

# In[26]:
    
prob = svm_problem(y_train.ravel(), x_train)
param = svm_parameter('-t 0 -c 0.0001')
model_1 = svm_train(prob, param)
p_label, p_acc, p_val = svm_predict(y_test.ravel(), x_test, model_1, '-q')
ACC, MSE, SCC = evaluations(y_test.ravel(), p_label)
print("SVM kernel=Linear C=0.0001 acc=" + str(ACC) + " n=" + str(model_1.get_nr_sv()))

prob = svm_problem(y_train.ravel(), x_train)
param = svm_parameter('-t 0 -c 0.05')
model_2 = svm_train(prob, param)
p_label, p_acc, p_val = svm_predict(y_test.ravel(), x_test, model_2, '-q')
ACC, MSE, SCC = evaluations(y_test.ravel(), p_label)
print("SVM kernel=Linear C=0.05 acc=" + str(ACC) + " n=" + str(model_2.get_nr_sv()))

prob = svm_problem(y_train.ravel(), x_train)
param = svm_parameter('-t 0 -c 0.1')
model_3 = svm_train(prob, param)
p_label, p_acc, p_val = svm_predict(y_test.ravel(), x_test, model_3, '-q')
ACC, MSE, SCC = evaluations(y_test.ravel(), p_label)
print("SVM kernel=Linear C=0.1 acc=" + str(ACC) + " n=" + str(model_3.get_nr_sv()))

prob = svm_problem(y_train.ravel(), x_train)
param = svm_parameter('-t 0 -c 2')
model_4 = svm_train(prob, param)
p_label, p_acc, p_val = svm_predict(y_test.ravel(), x_test, model_4, '-q')
ACC, MSE, SCC = evaluations(y_test.ravel(), p_label)
print("SVM kernel=Linear C=2 acc=" + str(ACC) + " n=" + str(model_4.get_nr_sv()))

prob = svm_problem(y_train.ravel(), x_train)
param = svm_parameter('-t 0 -c 5')
model_5 = svm_train(prob, param)
p_label, p_acc, p_val = svm_predict(y_test.ravel(), x_test, model_5, '-q')
ACC, MSE, SCC = evaluations(y_test.ravel(), p_label)
print("SVM kernel=Linear C=5 acc=" + str(ACC) + " n=" + str(model_5.get_nr_sv()))


# ## Step 2

# In[22]:



prob = svm_problem(y_train.ravel(), x_train)
param = svm_parameter('-t 0 -c 4')
model_6 = svm_train(prob, param)
p_label, p_acc, p_val = svm_predict(y_test.ravel(), x_test, model_6, '-q')
ACC, MSE, SCC = evaluations(y_test.ravel(), p_label)
print("SVM kernel=Linear C=4 acc=" + str(ACC) + " n=" + str(model_6.get_nr_sv()))

prob = svm_problem(y_train.ravel(), x_train)
param = svm_parameter('-t 1 -c 4')
model_7 = svm_train(prob, param)
p_label, p_acc, p_val = svm_predict(y_test.ravel(), x_test, model_7, '-q')
ACC, MSE, SCC = evaluations(y_test.ravel(), p_label)
print("SVM kernel=Polynomial C=4 acc=" + str(ACC) + " n=" + str(model_7.get_nr_sv()))

prob = svm_problem(y_train.ravel(), x_train)
param = svm_parameter('-t 2 -c 4')
model_8 = svm_train(prob, param)
p_label, p_acc, p_val = svm_predict(y_test.ravel(), x_test, model_8, '-q')
ACC, MSE, SCC = evaluations(y_test.ravel(), p_label)
print("SVM kernel=RBF C=4 acc=" + str(ACC) + " n=" + str(model_8.get_nr_sv()))

prob = svm_problem(y_train.ravel(), x_train)
param = svm_parameter('-t 3 -c 4')
model_9 = svm_train(prob, param)
p_label, p_acc, p_val = svm_predict(y_test.ravel(), x_test, model_9, '-q')
ACC, MSE, SCC = evaluations(y_test.ravel(), p_label)
print("SVM kernel=Sigmoid C=4 acc=" + str(ACC) + " n=" + str(model_9.get_nr_sv()))

