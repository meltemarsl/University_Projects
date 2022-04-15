#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
import numpy as np
import pandas as pd
import string


# In[3]:


test_data= pd.read_csv("BC7-LitCovid-Dev.csv")
train_data= pd.read_csv("BC7-LitCovid-Train.csv")


# In[4]:


#preprocessing
def preprocessing(data):

    takl = data[["title", "abstract", "keywords", "label"]]

    takl["keywords"] = takl["keywords"].apply(lambda x: str(x).replace(";", " "))

    takl["body"] =takl[["title", "abstract", "keywords"]].agg(" ".join, axis=1)
    
    body_label= takl[["body", "label"]]
    
    #case folding

    body_label["body"] = body_label["body"].apply(lambda x: str(x).casefold())

    #punctuation removal

    body_label["body"] = body_label["body"].apply(lambda x: str(x).translate(str.maketrans('', '', string.punctuation)))

    #tokenize

    body_label["body"] = body_label["body"].apply(lambda x: word_tokenize(str(x)))

    #stopword removal

    stop_words = set(stopwords.words('english'))

    for i in range(len(body_label)):
        body_label["body"][i]= [w for w in body_label["body"][i] if not w in stop_words]

    #lemmatization

    lemmatizer = WordNetLemmatizer()
    for i in range(len(body_label)):
        body_label["body"][i]= [lemmatizer.lemmatize(str(w)) for w in body_label["body"][i] ]

    #stemming

    sno = nltk.stem.SnowballStemmer('english')
    for i in range(len(body_label)):
        body_label["body"][i]= [sno.stem(str(w)) for w in body_label["body"][i] ]
        
    return body_label
    

#df['a'] = df['a'].apply(lambda x: x + 1)
#df['period'] = df[['Year', 'quarter', ...]].agg('-'.join, axis=1)


# In[5]:


preprocessed_test = preprocessing(test_data)
preprocessed_train = preprocessing(train_data)


# In[ ]:


import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline


# In[ ]:


X_train = preprocessed_train["body"]
Y_train = preprocessed_train["label"]

X_test = preprocessed_test["body"]
Y_test = preprocessed_test["label"]


# In[ ]:


X_train_str = ["" for x in range(len(X_train))]
X_test_str = ["" for x in range(len(X_test))]
strr = " "
for i in range(len(X_train)):
  string = ""
  for j in X_train.loc[i]:
    strr  += j
    string += j
    string += " "
  X_train_str[i] = string

for i in range(len(X_test)):
  string = ""
  for j in X_test.loc[i]:
    string += j
    string += " "
  X_test_str[i] = string


# In[ ]:


Y_train_CaseReport = np.zeros(len(Y_train))
Y_train_Diagnosis = np.zeros(len(Y_train))
Y_train_EpidemicForecasting = np.zeros(len(Y_train))
Y_train_Mechanism = np.zeros(len(Y_train))
Y_train_Prevention = np.zeros(len(Y_train))
Y_train_Transmission = np.zeros(len(Y_train))
Y_train_Treatment = np.zeros(len(Y_train))

for i in range(len(Y_train)):
  if 'Case Report' in Y_train[i]:
    Y_train_CaseReport[i] = 1
  if 'Diagnosis' in Y_train[i]:
    Y_train_Diagnosis[i] = 1
  if 'Epidemic Forecasting' in Y_train[i]:
    Y_train_EpidemicForecasting[i] = 1
  if 'Mechanism' in Y_train[i]:
    Y_train_Mechanism[i] = 1
  if 'Prevention' in Y_train[i]:
    Y_train_Prevention[i] = 1
  if 'Transmission' in Y_train[i]:
    Y_train_Transmission[i] = 1
  if 'Treatment' in Y_train[i]:
    Y_train_Treatment[i] = 1


# In[ ]:


Y_test_CaseReport = np.zeros(len(Y_test))
Y_test_Diagnosis = np.zeros(len(Y_test))
Y_test_EpidemicForecasting = np.zeros(len(Y_test))
Y_test_Mechanism = np.zeros(len(Y_test))
Y_test_Prevention = np.zeros(len(Y_test))
Y_test_Transmission = np.zeros(len(Y_test))
Y_test_Treatment = np.zeros(len(Y_test))

for i in range(len(Y_test)):
  if 'Case Report' in Y_test[i]:
    Y_test_CaseReport[i] = 1
  if 'Diagnosis' in Y_test[i]:
    Y_test_Diagnosis[i] = 1
  if 'Epidemic Forecasting' in Y_test[i]:
    Y_test_EpidemicForecasting[i] = 1
  if 'Mechanism' in Y_test[i]:
    Y_test_Mechanism[i] = 1
  if 'Prevention' in Y_test[i]:
    Y_test_Prevention[i] = 1
  if 'Transmission' in Y_test[i]:
    Y_test_Transmission[i] = 1
  if 'Treatment' in Y_test[i]:
    Y_test_Treatment[i] = 1


# In[ ]:


KNN = KNeighborsClassifier(n_neighbors=7)

# Pipeline =  CountVectorizer + TfidfTransformer + KNNClassifier
clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', KNN),])

clf.fit(X_train_str, Y_train_CaseReport)
predicted_CaseReport = clf.predict(X_test_str)
print('We got an accuracy of',np.mean(predicted_CaseReport == Y_test_CaseReport)*100, '% over the test data.')

clf.fit(X_train_str, Y_train_Diagnosis)
predicted_Diagnosis = clf.predict(X_test_str)
print('We got an accuracy of',np.mean(predicted_Diagnosis == Y_test_Diagnosis)*100, '% over the test data.')

clf.fit(X_train_str, Y_train_EpidemicForecasting)
predicted_EpidemicForecasting = clf.predict(X_test_str)
print('We got an accuracy of',np.mean(predicted_EpidemicForecasting == Y_test_EpidemicForecasting)*100, '% over the test data.')

clf.fit(X_train_str, Y_train_Mechanism)
predicted_Mechanism = clf.predict(X_test_str)
print('We got an accuracy of',np.mean(predicted_Mechanism == Y_test_Mechanism)*100, '% over the test data.')

clf.fit(X_train_str, Y_train_Prevention)
predicted_Prevention = clf.predict(X_test_str)
print('We got an accuracy of',np.mean(predicted_Prevention == Y_test_Prevention)*100, '% over the test data.')

clf.fit(X_train_str, Y_train_Transmission)
predicted_Transmission = clf.predict(X_test_str)
print('We got an accuracy of',np.mean(predicted_Transmission == Y_test_Transmission)*100, '% over the test data.')

clf.fit(X_train_str, Y_train_Treatment)
predicted_Treatment = clf.predict(X_test_str)
print('We got an accuracy of',np.mean(predicted_Treatment == Y_test_Treatment)*100, '% over the test data.')


# In[ ]:


trueLabels = 0
for i in range(len(Y_test)):
  if((predicted_CaseReport[i] == Y_test_CaseReport[i]) and (predicted_Diagnosis[i] == Y_test_Diagnosis[i]) and
     (predicted_EpidemicForecasting[i] == Y_test_EpidemicForecasting[i]) and (predicted_Mechanism[i] == Y_test_Mechanism[i]) and
     (predicted_Prevention[i] == Y_test_Prevention[i]) and (predicted_Transmission[i] == Y_test_Transmission[i]) and
     (predicted_Treatment[i] == Y_test_Treatment[i])):
    trueLabels+=1
print(trueLabels/len(Y_test))


# In[ ]:


import csv  

header = ['PMID','Treatment', 'Diagnosis',	'Prevention',	'Mechanism',	'Transmission',	'Epidemic Forecasting',	'Case Report']

with open('predicted_labels.csv', 'w', encoding='UTF8') as f:

  writer = csv.writer(f)

  # write the header
  writer.writerow(header)
  
  for i in range(len(Y_test)):
    data = [i, predicted_Treatment[i], predicted_Diagnosis[i], predicted_Prevention[i], predicted_Mechanism[i], 
            predicted_Transmission[i], predicted_EpidemicForecasting[i], predicted_CaseReport[i]]
    writer.writerow(data)


# In[ ]:


header = ['PMID','Treatment', 'Diagnosis',	'Prevention',	'Mechanism',	'Transmission',	'Epidemic Forecasting',	'Case Report']

with open('gold_labels.csv', 'w', encoding='UTF8') as f:

  writer = csv.writer(f)

  # write the header
  writer.writerow(header)
  
  for i in range(len(Y_test)):
    data = [i, Y_test_Treatment[i], Y_test_Diagnosis[i], Y_test_Prevention[i], Y_test_Mechanism[i], 
            Y_test_Transmission[i], Y_test_EpidemicForecasting[i], Y_test_CaseReport[i]]
    writer.writerow(data)

