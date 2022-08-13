#!/usr/bin/env python
# coding: utf-8

# ## importing all necessory libraries

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
from num2words import num2words


# In[2]:


#accessing all required files
with open('../pickle files/doc_fre.pkl','rb') as file:
    doc_fre=pickle.load(file)
    file.close()
    
with open('../pickle files/files_with_index.pkl','rb') as file:
    file_with_index=pickle.load(file)
    file.close()
    
with open('../pickle files/doc_word.pkl','rb') as file:
    doc_words=pickle.load(file)
    file.close()
    
with open('../pickle files/doc_norm.pkl','rb') as file:
    doc_norm=pickle.load(file)
    file.close()

with open('../pickle files/posting_list.pkl','rb') as file:
    posting_list=pickle.load(file)
    file.close()
    
with open('../pickle files/doc_len.pkl','rb') as file:
    doc_len=pickle.load(file)
    file.close()


# In[3]:


#calculating average document length
k=0
N=len(file_with_index)
for i in doc_len:
    k+=doc_len[i]
Lavg=k/N
#Lavg


# In[4]:


# using dictionary for faster access
from nltk.corpus import stopwords
li=stopwords.words('english')
Stopwords={}
for i in li:
    Stopwords[i]=1


# ##### &emsp; $\text{Getting the BM25 score for all documents}$
# ##### &emsp; &emsp; $score(D,Q) = \sum_{i=1}^nidf(q_i).\bigg(\frac{TF(q_i,D).(k+1)}{TF(q_i,D)+k.\big(1-b+b.\frac{|D|}{Lavg}\big)}\bigg)$
# ##### &emsp; &emsp; &emsp;$score(D,Q):\text{BM25 score for document } D \text{ for query }Q$
# ##### &emsp; &emsp; &emsp;$TF(q_i,D):\text{term frequency of }(q_i)\text{ in document}D$
# ##### &emsp; &emsp; &emsp;$|D|:\text{number of words in document D}$
# ##### &emsp; &emsp; &emsp;$Lavg:\text{average length of documents}$

# ##### &emsp; $\text{Calculating inverse document frequency for BM25 score}$
# ##### &emsp; &emsp; $idf(q_i) = log\big(\frac{N-n(q_i)+0.5}{n(q_i)+0.5}+1\big)$
# ##### &emsp; &emsp; &emsp;$idf(q_i):\text{inverse document frequency of query }(q_i)$
# ##### &emsp; &emsp; &emsp;$N:\text{Number of documents}$
# ##### &emsp; &emsp; &emsp;$n(q_i):\text{number of documents containing }(q_i)$

# In[5]:



def bm_for(q,TF,i):
    #calculating idf
    n_qi=0
    if q in doc_fre:
        n_qi=doc_fre[q]
    idf=math.log(((N-n_qi+0.5)/(n_qi+0.5))+1)
    #using bm25 formula.
    ans=idf*((k+1)*TF/(TF+k*(1-b+b*(doc_len[i]/Lavg))))
    return ans

def cal_score(words):
    for i in range(len(file_with_index)):
        score[i]=0
        for qi in words:
            TF=0
            if qi in posting_list:
                if i in posting_list[qi]:
                    TF=posting_list[qi][i]
            score[i]+=bm_for(qi,TF,i)
            
#calculate total score for query
def score_doc(q):
    #remove the punctuations
    text = re.sub(r'[^\w\s]',' ',q)
    # removing nonascii characters
    encoded_string = text.encode("ascii", "ignore")
    text = encoded_string.decode()
    # tokenizing the doc texts
    tokenize_words=word_tokenize(text)
    # lower all the words
    tokenize_words = [word.lower() for word in tokenize_words]
    #procedure to convert num to words
    temp=[]
    for w in tokenize_words:
        try:
            w=num2words(int(w))
        except:
            pass
        temp.append(w)
    tokenize_words=temp
    # stemming each word
    tokenize_words = [ps.stem(word) for word in tokenize_words]
    #removing all stopwords from query
    words=[word for word in tokenize_words if word not in Stopwords]
    #remove all unnecessory words which not present in any dictionary
    words=[word for word in tokenize_words if word in posting_list.keys()]
    print(words)
    cal_score(words)
        
k=1.2
b=0.75


# In[6]:


score={}
query=input("Enter your query: ")
for i in range(len(file_with_index)):
    score[i]=0
#calculating score according to BM25 formula
score_doc(query)
#sorting the dictionary according to score
score=sorted(score.items(),key=lambda item: item[1],reverse=True)
# print(score)
#print top 10 document according to score
count = 10
for i in score:
    if count == 0:
        break
    print(file_with_index[i[0]],i[1])
    count-=1


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




