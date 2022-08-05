#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import pickle
import os
from numpy.lib.function_base import vectorize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import string
from nltk import PorterStemmer
from nltk.stem import WordNetLemmatizer

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
  lower_case = text.lower()
  wh_special_char = lower_case.translate(str.maketrans(string.punctuation,' '*len(string.punctuation)))
  cleaned_data = ""
  for word in wh_special_char.split():
    if word not in stop_words:
      cleaned_data += " " + lemmatizer.lemmatize(word)
  return cleaned_data



if len(sys.argv) != 3:
  print("Three arguments expected.")
  exit()
pkl_filename = sys.argv[1]
FILE_PATH = sys.argv[2]

with open(pkl_filename, "rb") as file:
  vectorizer = pickle.load(file)
  clf = pickle.load(file)

# read test data
data = []
labels = []
dirs = os.listdir(FILE_PATH)
dirsSorted = sorted(dirs, key=lambda filename:int(filename[:-6]))
for file in dirsSorted:
  filename=os.path.join(FILE_PATH,file)
  f = open(filename, "r", encoding="latin-1")
  text = f.read()
  data.append(clean_data(text))
  labels.append(file[-5])
  f.close()


features = vectorizer.transform(data)
prediction = clf.predict(features)
print("".join(prediction))

