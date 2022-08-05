### Sentiment Analysis on IMDB User Reviews


## BEFORE RUNNING

$ python3 -m pip install -r requirements.txt


## TRAINING

There should be a training set in the directory "TRAIN" for this to work.

$ python3 train.py

Output: Performance metric values (accuracy, precision, recall, macro average).

All code for training resides in train.py. Models we tried are commented out, only the best one is uncommented. If you want to train a different model than the best one, make sure that the vectorizer (Count or Tf Idf) is set and model is uncommented.

GLOVE: 
$ python3 glove.py

BERT:
$ python3 BERT.py

Word2vec:
Uncomment lines =  [250-267]
$ python -m spacy download en_core_web_sm
$ python3 train.py


## TESTING

$ python3 Step3_Solis.py model.pkl TEST

Output: A string consisting of P,N,Z characters representing predicted class of each document.
