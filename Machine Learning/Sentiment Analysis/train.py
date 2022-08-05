#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import matplotlib.pyplot as plt
import array as arr
import string
import os
import pickle
from wordcloud import WordCloud
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
              "does", "did", "doing", "a", "an", "the", "but", "and", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about","against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under",
              "further", "then", "once", "here", "there", "when", "where", "all", "both", "each", "few", "more",
              "other", "some", "such", "only", "own",  "so", "than", "s", "t", "can", "will", "just", "don", "now",
              "br", "39", "quot", "one", "seen", "ve", "film", "movie", "story", "one", "character", "time", "movies",
              "character","thing","people", "make"]



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
      cleaned_data += " " + lemmatizer.lemmatize(word)
  return cleaned_data

def print_metrics(prediction, labels):
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
  print("\nOverall Accuracy: " + str(sum(tp.values())/N))
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
  print("\nClass Accuracies:")
  print(accuracy)
  print("\nClass Precisions:")
  print(precision)
  print("\nClass Recalls:")
  print(recall)
  print("\nMacro average accuracy: ")
  print(sum(accuracy.values()) / 3)
  print("\nMacro average precision: ")
  print(sum(precision.values()) / 3)
  print("\nMacro average recall: ")
  print(sum(recall.values()) / 3)

#def get_word_clouds(data_p, data_n, data_z):
 # word cloud images for insight into data
  # negative
#  word_cloud = WordCloud(collocation_threshold=30).generate(text = data_n)
#  plt.imshow(word_cloud, interpolation= "bilinear")
#  plt.savefig("negative_wordcloud.png")
#  # positive
#  word_cloud = WordCloud(collocation_threshold=30).generate(text = data_p)
#  plt.imshow(word_cloud, interpolation= "bilinear")
#  plt.savefig("positive_wordcloud.png")
  # neutral
#  word_cloud = WordCloud(collocation_threshold=30).generate(text = data_z)
#  plt.imshow(word_cloud, interpolation= "bilinear")
#  plt.savefig("neutral_wordcloud.png")

# word cloud for each class using bigrams
# change 
#get_word_clouds(data_p, data_n, data_z)

#read the data
data = []
labels=[]
# variables to store data for word cloud
data_z = data_n = data_p = ""
FILE_PATH = "TRAIN/"
dirs = os.listdir(FILE_PATH)
dirsSorted = sorted(dirs, key=lambda filename:int(filename[:-6]))
for file in dirsSorted:
  filename=os.path.join(FILE_PATH,file)
  f = open(filename, "r", encoding="latin-1")
  text = f.read()
  text = clean_data(text)
  data.append(text)
  if file[-5] == "N":
    data_n += text
  elif file[-5] == "Z":
    data_z += text
  elif file[-5] == "P":
    data_p += text
  labels.append(file[-5])
  f.close()

#TF-IDF + SVM
vectorizer = TfidfVectorizer()
features = vectorizer.fit_transform(data)

# initiate model
clf = svm.SVC()

# train
clf.fit(features, labels)

# get the training accuracy
prediction = clf.predict(features)
print_metrics(prediction, labels)
with open("step3_model_Solis.pkl", "wb") as file:
  pickle.dump(vectorizer, file)
  pickle.dump(clf, file)



# Other methods
# We used three methods to vectorize
# 1) Count Vectorizer (binary option being True or False),  2) Tf Idf Vectorizer, 3) First two pipelined
# and three models
# 1) Naive Bayes, 2) Logistic Regression, 3) SVM
# (not all combinations)

### bag of words

# uncomment following two lines if you want to try a model with Count
#count = CountVectorizer()
#bag = count.fit_transform(data)

# use binary parameter for binary count (1 if word is in document, 0 otherwise)
# uncomment following two lines if you want to try a model with Binary Count
#count_bin = CountVectorizer(binary=True)
#bag_bin = count.fit_transform(data)

# now we can use the vectorized data (bag/bag_bin) with different models



# Naive Bayes + Count
#clf = MultinomialNB()
#clf.fit(bag.toarray(), labels)
#prediction = clf.predict(bag.toarray())
#print_metrics(prediction, labels)



# Naive Bayes + Binary Count
#clf = MultinomialNB()
#clf.fit(bag_bin.toarray(), labels)
#prediction = clf.predict(bag_bin.toarray())
#print_metrics(prediction, labels)



# SVM + Count
#clf = svm.SVC()
#clf.fit(bag.toarray(), labels)
#prediction = clf.predict(bag.toarray())
#print_metrics(prediction)





# Naive Bayes + Count + TfIdf
#transformVectorizer = TfidfTransformer()
#transformed = transformVectorizer.fit_transform(bag)
#clf = MultinomialNB()
#clf.fit(transformed, labels)
#prediction = clf.predict(transformed)
#print_metrics(prediction)




# Naive Bayes + Binary Count + TfIdf
#transformVectorizer = TfidfTransformer()
#transformed = transformVectorizer.fit_transform(bag_bin)
#clf = MultinomialNB()
#clf.fit(transformed, labels)
#prediction = clf.predict(transformed)
#print_metrics(prediction)




# Logistic Regression + TfIdf
#clf = LogisticRegression(random_state=0, solver='lbfgs')
#clf.fit(features, labels)
#prediction = clf.predict(features)
#print_metrics(prediction)




# SVM + TfIdf
#clf = svm.SVC()
#clf.fit(features, labels)
#prediction = clf.predict(features)
#print_metrics(prediction



#word2vec + SVM

#import spacy
# Load the spacy model that you have installed
#nlp = spacy.load('en_core_web_sm')

#features = []
#for i in data:
#    doc = nlp(i)
#    features.append(doc.vector)
    
# initiate model
#clf = svm.SVC(kernel='rbf', C=15)

# train
#clf.fit(features, labels)

# get the training accuracy
#prediction = clf.predict(features)
#print_metrics(prediction, labels)


# In[ ]:




