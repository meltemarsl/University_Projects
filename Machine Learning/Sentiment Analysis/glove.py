import numpy as np
import matplotlib.pyplot as plt
import array as arr
import string
import os
import pickle
#from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from nltk import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression

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
              "br", "39", "quot", "one", "seen", "ve", "film", "movie", "one", "character", "time", "movies"]


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
  print("Overall Accuracy: " + str(sum(tp.values())/N) + "\n")
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
  return sum(tp.values())/N


data = []
labels=[]
FILE_PATH = "TRAIN/"
dirs = os.listdir(FILE_PATH)
dirsSorted = sorted(dirs, key=lambda filename:int(filename[:-6]))
for file in dirsSorted:
  filename=os.path.join(FILE_PATH,file)
  f = open(filename, "r", encoding="latin-1")
  text = f.read()
  text = clean_data(text)
  data.append(text)
  labels.append(file[-5])
  f.close()

data_val = []
labels_val =[]
FILE_PATH = "VAL/"
for file in os.listdir(FILE_PATH):
  filename=os.path.join(FILE_PATH,file)
  f = open(filename, "r", encoding="latin-1")
  text = f.read()
  text = clean_data(text)
  data_val.append(text)
  labels_val.append(file[-5])
  f.close()

def get_doc_vector(doc):
    vec = np.zeros(50) # to be changed if you use different word vec model
    ct = 0
    docArr = doc.split()
    for i in range(len(docArr)-1):
      e1 = docArr[i]
      e2 = docArr[i+1]
      try:
          vec += (glove_vectors[e1]+glove_vectors[e2])/2
          ct+=1
      except Exception as e:
          print(e)
          continue
    if ct == 0:
        return vec
    else:
        return vec/ct

import gensim.downloader
glove_vectors = gensim.downloader.load('glove-wiki-gigaword-50')

vectors = []
for row in data:
  vectors.append(get_doc_vector(row))
vectors_val = []
for row in data_val:
  vectors_val.append(get_doc_vector(row))

# initiate model
clf_glove2 = svm.SVC()

# train
clf_glove2.fit(vectors, labels)

prediction_glove2 = clf_glove2.predict(vectors)
print_metrics(prediction_glove2,labels)

prediction_glove2_val = clf_glove2.predict(vectors_val)
print_metrics(prediction_glove2_val,labels_val)
