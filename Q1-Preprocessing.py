#!/usr/bin/env python
# coding: utf-8

# ## Importing all necessory libraries

# In[1]:


import numpy as np
import os
import sys
import re
import math
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import sent_tokenize , word_tokenize
import glob
from pathlib import Path
from collections import Counter
ps=PorterStemmer()


# In[2]:


### Store stopwords into dictioary for faster access
li=stopwords.words('english')
Stopwords={}
for i in li:
    Stopwords[i]=1


# In[3]:


#defining necessory list and dictionary
list_of_all_words=[]
doc_words=[]
all_unique_words={}
def numToWords(words):
    temp=[]
    for w in words:
        try:
            w=num2words(int(w))
        except:
            pass
        temp.append(w)
    return temp


# In[4]:


#accessing all txt files
file_folder = './english-corpora/*'
index = 0
files_with_index = {}
#defining stemming obj
ps = PorterStemmer()
for file in glob.glob(file_folder):
    fname = file
    #opening the file
    file = open(file , "r",encoding='UTF-8')
    #reading the text file
    text = file.read()
    #remove the punctuations
    text = re.sub(r'[^\w\s]',' ',text)
    # removing nonascii characters
    encoded_string = text.encode("ascii", "ignore")
    text = encoded_string.decode()
    # tokenizing the doc texts
    words=word_tokenize(text)
    # remove words which len is less than 1
    words = [word for word in words if len(word)>1]
    # lower all the words
    words = [word.lower() for word in words]
    #procedure to convert num to words
    temp=[]
    for w in words:
        try:
            w=num2words(int(w))
        except:
            pass
        temp.append(w)
    words=temp
    # stemming each word
    words = [ps.stem(word) for word in words]
    # remove stop words from tokenize_words list
    words = [word for word in words if word not in Stopwords]
    #storing words for each document
    doc_words.append(words)
    #this used to collect unique word
    for i in words:
        all_unique_words[i]=1
    #storing file index
    files_with_index[index]=os.path.basename(fname)
    print(index)
    index=index+1
    
#getting all unique words
unique_words_all = set(all_unique_words.keys())


# In[5]:


len(all_unique_words)


# In[6]:


#defining posting list(each key is uniqueword and corresponding value is another dictinary which having document id as key and unique word occurences in that document)
posting_list={} #simply it having all document index which having that words with their frequency in that document 
doc_fre={}#it store frequency of word in all documents
#iterate over all unique words
for i in unique_words_all:
    posting_list[i]={}
    doc_fre[i]=0
#iterating over each txt files
file_folder = './english-corpora'
pathlist = Path(file_folder).rglob('*.txt')
index=0
doc_len={}
for path in pathlist:
    filename = str(path)
    #opening the file
    file = open(file , "r",encoding='UTF-8')
    #reading the text file
    text = file.read()
    #remove the punctuations
    text = re.sub(r'[^\w\s]',' ',text)
    # removing nonascii characters
    encoded_string = text.encode("ascii", "ignore")
    text = encoded_string.decode()
    # tokenizing the doc texts
    words=word_tokenize(text)
    # remove words which len is less than 1
    words = [word for word in words if len(word)>1]
    # lower all the words
    words = [word.lower() for word in words]
    #procedure to convert num to words
    temp=[]
    for w in words:
        try:
            w=num2words(int(w))
        except:
            pass
        temp.append(w)
    words=temp
    # stemming each word
    words = [ps.stem(word) for word in words]
    # remove stop words from tokenize_words list
    words = [word for word in words if word not in Stopwords]
    # calulating and storing doc len
    doc_len[index]=len(words)
    counter=Counter(words)
    for i in counter.keys():
        if i not in doc_fre:
            doc_fre[i]=0
            posting_list[i]={}
        doc_fre[i]=doc_fre[i]+1
        posting_list[i][index]=counter[i]   
    print(index)
    index=index+1


# In[7]:


#storing l2-norm of each document which is used in TF-IDF to find cosine similarity score.
doc_norm={}
index=0
#doc_words store all words in corresponing document 
for i in doc_words:
    l2=0
    print(index)
    for j in set(i):
        l2+=(i.count(j)*math.log(len(files_with_index)/doc_fre[j]))**2
    doc_norm[index]=(math.sqrt(l2))
    index+=1


# In[8]:


#store all required data that can used in other questions for faster processing.
with open('posting_list.pkl','wb') as file:
    pickle.dump(posting_list,file)
    file.close()

#storing freuency of words in all documents using dictionary(key:words,value:frequency of that words over all document)
with open('doc_fre.pkl','wb') as file:
    pickle.dump(doc_fre,file)
    file.close()
    
#storing each document length
with open('doc_len.pkl','wb') as file:
    pickle.dump(doc_len,file)
    file.close()

#storing all words present in particular document
with open('doc_word.pkl','wb') as file:
    pickle.dump(doc_words,file)
    file.close()

#storing all unique words over all document
with open('unique_words_all.pkl','wb') as file:
    pickle.dump(unique_words_all,file)
    file.close()

#storing index and correspoing name of document
with open('files_with_index.pkl','wb') as file:
    pickle.dump(files_with_index,file)
    file.close()

#storing l2-norm for each document which can use further
with open('doc_norm.pkl','wb') as file:
    pickle.dump(doc_norm,file)
    file.close()


# In[9]:



