#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install bert-for-tf2')
get_ipython().system('pip install sentencepiece')


# In[2]:


try:
    get_ipython().run_line_magic('tensorflow_version', '2.x')
except Exception:
    pass
import tensorflow as tf

import tensorflow_hub as hub

from tensorflow.keras import layers
import bert


# In[3]:


BertTokenizer = bert.bert_tokenization.FullTokenizer


# In[4]:


bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/1",
                            trainable=False)


# In[5]:


vocabulary_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
to_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
tokenizer = BertTokenizer(vocabulary_file, to_lower_case)


# In[24]:


import nltk
nltk.download('wordnet')

import numpy as np
import matplotlib.pyplot as plt
import array as arr
import string
import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from nltk import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under",
              "further", "then", "once", "here", "there", "when", "where", "all", "both", "each", "few", "more",
              "other", "some", "such", "only", "own",  "so", "than", "s", "t", "can", "will", "just", "don", "now",
              "br", "39", "quot", "one", "seen", "ve", "film", "movie", "story", "one", "character", "time", "movies"]



def clean_data(text):
    """
    processes the given string:
    - convert to lower case
    - remove punctuation
    - remove stop words
    - lemmatize

    :text: string which is the content of a comment file
    :return: processed string
    """
    lower_case = text.lower()
    wh_special_char = lower_case.translate(str.maketrans(string.punctuation,' '*len(string.punctuation)))
    cleaned_data = ""
    for word in wh_special_char.split():
        if word not in stop_words:
            #cleaned_data += " " + lemmatizer.lemmatize(word)
            cleaned_data += " " + word
    return cleaned_data

def print_metrics(prediction, labels):
    """
    Prints accuracy, precision, recall, and macro average values given predictions and labels.
    :prediction: array of strings, each element is one of the "P", "N", or "Z"
    :labels: same format as prediction
    """
    N = len(labels)
    count = {"P":0, "N":0, "Z":0}
    labelCount = {"P":0, "N":0, "Z":0}
    tp = {"P":0, "N":0, "Z":0}
    tn = {"P":0, "N":0, "Z":0}
    classes = ["P", "N", "Z"]
    for i in range(N):
        count[prediction[i]] += 1
        labelCount[labels[i]] += 1
        if prediction[i] == labels[i]:
            tp[prediction[i]] += 1
        for c in classes:
            if c != prediction[i] and c != labels[i]:
                tn[c] += 1
    accuracy = {"P":0, "N":0, "Z":0}
    precision = {"P":0, "N":0, "Z":0}
    recall = {"P":0, "N":0, "Z":0}
    print("Overall Accuracy: " + str(sum(tp.values())/N)+"\n")
    for i in ["P", "N", "Z"]:
        if count[i] == 0:
            precision[i] = 1
        else:
            precision[i] = tp[i]/count[i]
        if labelCount[i] == 0:
            recall[i] = 1
        else:
            recall[i] = tp[i]/labelCount[i]
        accuracy[i] = (tp[i] + tn[i])/N
  #print("\nClass Accuracies:")
  #print(accuracy)
  #print("\nClass Precisions:")
  #print(precision)
  #print("\nClass Recalls:")
  #print(recall)
  #print("\nMacro average accuracy: ")
  #print(sum(accuracy.values()) / 3)
  #print("\nMacro average precision: ")
  #print(sum(precision.values()) / 3)
  #print("\nMacro average recall: ")
  #print(sum(recall.values()) / 3)
    return sum(tp.values())/N




min_tok_id=50000
max_tok_id=0
a=0
data = []
labels=[0]*3000
# variables to store data for word cloud
data_z = data_n = data_p = ""
FILE_PATH = "TRAIN/"
for file in os.listdir(FILE_PATH):
    filename=os.path.join(FILE_PATH,file)
    f = open(filename, "r", encoding="latin-1")
    text = f.read()
    text = clean_data(text)
    data.append(" ".join(tokenizer.tokenize(text)))
    if file[-5] == "N":
        data_n += text
    elif file[-5] == "Z":
        data_z += text
    elif file[-5] == "P":
        data_p += text
    labels[a]=(file[-5])
    f.close()
    a=a+1


# In[25]:


vectorizer = TfidfVectorizer()
features = vectorizer.fit_transform(data)

#clf = svm.SVC()
clf=LogisticRegression(random_state=0)

# train
clf.fit(features, labels)

# get the training accuracy
prediction = clf.predict(features)
print_metrics(prediction, labels)


# In[26]:


data_val = []
labels_val=[0]*750
a=0
FILE_PATH = "VAL/"
for file in os.listdir(FILE_PATH):
    filename=os.path.join(FILE_PATH,file)
    f = open(filename, "r", encoding="latin-1")
    text_val = f.read()
    text_val = clean_data(text_val)
    data_val.append(" ".join(tokenizer.tokenize(text_val)))
    labels_val[a]=(file[-5])
    f.close()
    a=a+1
    
features_val = vectorizer.transform(data_val)
prediction_val = clf.predict(features_val)
print_metrics(prediction_val, labels_val)

