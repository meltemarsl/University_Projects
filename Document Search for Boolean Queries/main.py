from bs4 import BeautifulSoup
import os
import string
import json


words = set()
stop_words = ["a","all","an","and","any","are","as","be","been","but","by","few","for","have","he","her","here","him","his",
              "how","i","in","is","it","its","many","me","my","none","of","on","or","our","she","some","the","their","them",
              "there","they","that","this","us","was","what","when","where","which","who","why","will","with","you","your"]

def clean_data(text):
    lower_case = text.lower()
    wh_special_char = lower_case.translate(str.maketrans(string.punctuation,' '*len(string.punctuation)))
    cleaned_data = ""
    for word in wh_special_char.split():
        if word not in stop_words:
            words.add(word)
            cleaned_data += " " + word
    return cleaned_data


path = os.getcwd()
files = []
for file in os.listdir(path):
    if os.path.isfile(os.path.join(path, file)):
        if(file.endswith(".sgm")):
            files.append(os.path.join(path,file))


def getIDs(f):
    IDsIndex = [i for i in range(len(f)) if f.startswith("NEWID", i)]
    IDs = []
    for i in IDsIndex:
        x = f[i+7:i+13]
        k =x.find("\"")
        IDofFile = x[:k]
        IDs.append(IDofFile)
    return IDs

#articles, titles and bodies without special character and stop words
def getCleanedArticle(articles0, articleID):
    if(articleID == 21):
        titles = [None] * 578
        bodies = [None] * 578
        articles = [None] * 578
    else:
        titles = [None] * 1000
        bodies = [None] * 1000
        articles = [None] * 1000
    for i in range(len(articles0)):
        s = BeautifulSoup(articles0[i],'html.parser')
        title = str(s.find('title'))
        body = str(s.find('body'))
        if(title != " "):
            title = title[7:-8]
        titles[i] = clean_data(title)
        if(body != " "):
            body = body[6:-7]
        bodies[i] = clean_data(body)
        articles[i] = clean_data(title + " " + body)
    return articles

def getArticles(f, articleID):
    reutersBegin = [i for i in range(len(f)) if f.startswith("<REUTERS", i)]
    reutersEnd = [i for i in range(len(f)) if f.startswith("</REUTERS>", i)]
    if(articleID == 21):
        articles0 = [None] * 578
    else:
        articles0 = [None] * 1000
    for i in range(len(reutersBegin)):
        articles0[i] = (f[reutersBegin[i]: reutersEnd[i]])
    return getCleanedArticle(articles0, articleID)
#articles0 has all the documents as a list element but beginning from 'reuters' so it should be cleaned

articles = [None] * 21578
for i in range(len(files)):
    with open(files[i], "r+", encoding="latin-1" ) as f:
        f = f.read()
        fileIDs = getIDs(f)
        articles[i*1000:i*1000+len(fileIDs)] = getArticles(f, i)

wordsList = list(words)
invertedIndexDict = {}
def getInvertedIndex(word):
    wordInArticles = []
    for i in range(len(articles)):
        wordsInArticle = [x.strip() for x in articles[i].split(' ')]
        if word in wordsInArticle:
            wordInArticles.append(i+1)
    invertedIndexDict[word] = wordInArticles

def intersect(w1, w2):
    answer = []
    l1 = invertedIndex[w1]
    l2 = invertedIndex[w2]
    len1 = len(l1)
    len2 = len(l2)
    if(len1<len2):
        for i in range(len1):
            if(l1[i] in l2):
                answer.append(l1[i])
    else:
        for i in range(len2):
            if(l2[i] in l1):
                answer.append(l2[i])
    return answer


def goAnd(query):
    wordsInQ = [x.strip() for x in query.split('AND')]
    nofWords = len(wordsInQ)
    i = 0
    for i in range(nofWords-1):
        if(i==0):
            answer = intersect(wordsInQ[i], wordsInQ[i+1])
        else:
            answer = intersect(x, wordsInQ[i+1])
    print(answer)
    return answer
def goNot(wanted, notQ):
    answer = []
    wordsInQ = [x.strip() for x in notQ.split('NOT')]
    for word in wordsInQ:
        l = invertedIndex[word]
        for i in range(len(wanted)):
            if(wanted[i] not in l):
                answer.append(wanted[i])
    return answer
def goAndNot(query):
    iNot = query.find('NOT')
    andQ = query[0:iNot]
    notQ = query[iNot:]
    wanted = goAnd(andQ)
    notWanted = goNot(wanted, notQ)
    return notWanted
def goOrNot(query):
    iNot = query.find('NOT')
    orQ = query[0:iNot]
    notQ = query[iNot:]
    wanted = goOr(orQ)
    notWanted = goNot(wanted, notQ)
    return notWanted
def goOr(query):
    answerS = set()
    wordsInQ = [x.strip() for x in query.split('OR')]
    for word in wordsInQ:
        t = invertedIndex[word]
        for i in t:
            answerS.add(i)
    answer = list(answerS)
    answer.sort()
    return answer

def parseQuery(query):
    if "AND" in query:
        if "NOT" in query:
            goAndNot(query)
        else:
            goAnd(query)
    elif "OR" in query:
        if "NOT" in query:
            goOrNot(query)
        else:
            goOr(query)
    else:
        print("Unsupported query operation. Please give a valid query.")

if __name__ == '__main__':
    try:
        with open('invIndex.json', "r") as f:
            invertedIndex = json.load(f)
    except IOError:
        for i in range(len(wordsList)):
            getInvertedIndex(wordsList[i])
        with open('invIndex.json', 'w') as f:
            f.write(json.dumps(invertedIndexDict))
            invertedIndex = invertedIndexDict
    while True:
        query = input("Enter your query: ")
        if (query == "Close"):
            break
        parseQuery(query)
