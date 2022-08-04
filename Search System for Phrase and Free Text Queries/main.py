#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import string
import os
import sys
import math
import json



#function for cleaning docs and also it fills the wordsDict dictionary while cleaning
#clean operations: caselowering, removing stopwords and punctuations
def clean_data(text, docID, wordsDict):
    lower_case = text.lower()
    wh_special_char = lower_case.translate(str.maketrans(string.punctuation,' '*len(string.punctuation)))
    cleaned_data = ""
    index = 0
    for word in wh_special_char.split():
        if word not in stop_words:
            try:
                docs = wordsDict[word]
            except:
                docs = {}
            try:
                indexes = docs[docID]
            except:
                indexes = []
            indexes.append(index)
            docs[docID] = indexes
            wordsDict[word] = docs
            cleaned_data += " " + word
            index += 1
    return cleaned_data


#returns the NEWIDs of the given file
def getIDs(f):
    IDsIndex = [i for i in range(len(f)) if f.startswith("NEWID", i)]
    IDs = []
    for i in IDsIndex:
        x = f[i+7:i+13]
        k =x.find("\"")
        IDofFile = x[:k]
        IDs.append(IDofFile)
    return IDs


# gets the file content, ID of the file and NEWIDs of that file as arguments and fills the corresponding part of the articles list
def getArticles(f, fileID, fileIDs, wordsDict):
    reutersBegin, reutersEnd = [i for i in range(len(f)) if f.startswith("<REUTERS", i)], [i for i in range(len(f)) if
                                                                                           f.startswith("</REUTERS>",
                                                                                                        i)]
    if (fileID == 21):
        currArt, titles, bodies, articles = [None] * 578, [None] * 578, [None] * 578, [None] * 578
    else:
        currArt, titles, bodies, articles = [None] * 1000, [None] * 1000, [None] * 1000, [None] * 1000

    for i in range(len(reutersBegin)):
        currArt[i] = (f[reutersBegin[i]: reutersEnd[i]])
        try:
            tBegin, tEnd = currArt[i].index("<TITLE"), currArt[i].index("</TITLE")
            title = currArt[i][tBegin + 7:tEnd]
        except:
            title = " "
        try:
            bBegin, bEnd = currArt[i].index("<BODY"), currArt[i].index("</BODY")
            body = currArt[i][bBegin + 6:bEnd - 11]
        except:
            body = " "
        articles[i] = clean_data(title + " " + body, fileIDs[i], wordsDict)
    return articles

#checks if an element is in the given list or not, returns boolean
def isIn(element, listt):
    for i in range(len(listt)):
        if(element < listt[i]):
            return False
        if(element == listt[i]):
            return True
    return False

#returns the common elements of given two sets
def intersect(set1, set2):
    commonDocs = set()
    for doc in set1.intersection(set2):
        commonDocs.add(doc)
    return commonDocs


def phraseQ(query, wordsDict):
    docs = []
    qWords = query.split()
    qDicts = [None]*len(qWords)
    qSets = [None]*len(qWords)
    for i in range(len(qWords)):
        qDicts[i] = wordsDict[qWords[i]]
        qSets[i] = set(qDicts[i])
    c = 0
    while(c < len(qWords)-1):
        if(c == 0):
            commonDocs = intersect(qSets[0], qSets[1])
        else:
            commonDocs = intersect(commonDocs, qSets[c+1])
        c+=1
    if(len(commonDocs) == 0):
        print("There is no common doc")
    else:
        #go through all docs one by one
        commonDocs = list(commonDocs)
        for i in range(len(commonDocs)):
            exists = True
            
            #list for the indexes of query words for this document
            indexes = [None]*len(qWords)
            
            for w in range(len(qWords)):
                word = qWords[w]
                currDoc = commonDocs[i]
                indexes[w] = wordsDict[word][currDoc] #get the places of query words for this document
            a = indexes
            for j in range(len(a)):
                a[j].append(j)
            a.sort(key = len)   #a: is a copy of indexes but also includes the places of query words with respect to each other as a last element
            
            for k in range(len(a[0])-1):
                exists = True
                for j in range(1, len(a)):
                    listt = a[j][:-1]  #listt:document indexes to be controled
                    if(not (isIn(a[0][k] - (a[0][-1]-a[j][-1]), listt))):
                        
                        exists = False
            if(exists):
                docs.append(commonDocs[i])
    return docs


# returns the docs which contains at least one query words as a list
def andDocs(query, wordsDict):
    docs = set()
    qWords = query.split()

    for word in qWords:
        try:
            x = wordsDict[word].keys()
        except:
            x = []
        for i in x:
            docs.add(i)
    return list(docs)

#returns tfidf value for a given word and a doc, if the doc does not includes the word returns 0
def tfidf(doc, word, wordsDict):
    try:
        result = (1+ math.log(len(wordsDict[word][doc]), 10)) * (math.log(21579/len(wordsDict[word]), 10))
    except:
        result = 0
    return result

#calculates and returns the tf-idf value for the query and given query word
def docTfidf(query, word, wordsDict):
    occ = 0
    for w in query:
        if w == word:
            occ+=1
    try:
        result = (1+ math.log(occ, 10)) * (math.log(21579/len(wordsDict[word]), 10))
    except:
        result = 0
    return result

#returns normalized table by dividing each row element to that row's l2 norm.
def normalizeTable(table, rows, cols):
    for row in range(rows):
        #print(table[row])
        summ = 0
        for col in range(cols):
            summ += (table[row][col]) * (table[row][col])
        sqrtSum = math.sqrt(summ)
        for col in range(cols):
            table[row][col] = table[row][col] / sqrtSum
    return table

#calculates the cosine similarity between the query and each doc which are represented as rows of the table
def getCosines(table, qrow, rows, cols):
    cosines = [None]*(rows-1)
    for row in range(rows-1):
        summ = 0
        for col in range(cols):
            summ+= table[row][col]*qrow[col]
        cosines[row] = summ
    return cosines


def freeTextQ(query, wordsDict):
    
    qDocs = andDocs(query, wordsDict)  #dDocs: documents containing at least one query word
    qWords = query.split()  #qWords: query words
    q = list(qWords)
    x = set(wordsDict.keys())
    x = list(x)
    for i in x:
        if i not in q:
            q.append(i)
    x = q                 # x: the list contains both dictionary words and query words. First words are query words
    nOfWords = len(x)
    rows, cols = (len(qDocs) + 1, nOfWords)
    table = []          #table to hold tf-idf values of word-document pairs
    
    #fills the table with zeros
    for r in range(rows):
        l = []
        for c in range(cols):
            l.append(0)
        table.append(l)

    # first row of the table holds the values for query vector
    for word in range(len(qWords)):
        table[0][word] = docTfidf(qWords, qWords[word], wordsDict)
    
    #remaining rows of the table holds the values for documents
    for doc in range(len(qDocs)):
        for word in range(nOfWords):
            table[doc+1][word] = tfidf(qDocs[doc], x[word], wordsDict)
            
    #normalize table rows
    normalizedT = normalizeTable(table, rows, cols)

    #get cosine similarities of each document(represented as table rows) with query vector(first row of the table)
    cosines = getCosines(normalizedT[1:], normalizedT[0], rows, cols)

    result = {}
    for i in range(len(cosines)):
        result[qDocs[i]] = cosines[i]
    
    #return results as dictionary to hold docIDs
    return result

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        #checks if the inverted index file is already created or not. Use it if exists
        with open('invIndex.json', "r") as f:
            wordsDict = json.load(f)
            print("Reading from file...")
    except IOError:
        
        wordsDict = {} #the dictionary which will include words, their docs and the indexes of each doc for the word
        stop_words = ["a","all","an","and","any","are","as","be","been","but","by","few","for","have","he","her","here","him","his",
              "how","i","in","is","it","its","many","me","my","none","of","on","or","our","she","some","the","their","them",
              "there","they","that","this","us","was","what","when","where","which","who","why","will","with","you","your"]
    
    # get the names of the files in the directory
        path = os.getcwd()
        files = []
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                if(file.endswith(".sgm")):
                    files.append(os.path.join(path,file))
        
        articles = [None] * 21578
        for i in range(len(files)):
            with open(files[i], "r+", encoding="latin-1") as f:
                f = f.read()
                fileIDs = getIDs(f)
                articles[i * 1000:i * 1000 + len(fileIDs)] = getArticles(f, i, fileIDs, wordsDict)
                
        with open('invIndex.json', 'w') as f:
            f.write(json.dumps(wordsDict))
            print("Writing to the file...")
    try:
        #checks if the inverted index file is already created or not. Use it if exists
        with open('invIndex.json', "r") as f:
            wordsDict = json.load(f)
            print("Reading from file...")
            while True:
                query = input("Enter your query: ")
                if query[0] == '\"':
                    query = query[1:-1]
                    r = phraseQ(query, wordsDict)
                    r.sort()
                    print(r)
                else:
                    result = freeTextQ(query, wordsDict)
                    result2 = {}
                    for x in result:
                        if result[x] != 0.00000:
                            result2[x] = result[x]
                    sorted_dict = {}
                    sorted_keys = sorted(result2, key=result2.get)
                    for keyy in sorted_keys:
                        sorted_dict[keyy] = result2[keyy]

                    dict_items = sorted_dict.items()
                    last_ten = list(dict_items)[-10:]
                    for i in range(10):
                        print(last_ten[9-i])
    except IOError:
        print("could not read")

