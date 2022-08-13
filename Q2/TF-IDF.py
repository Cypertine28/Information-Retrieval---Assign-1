#!/usr/bin/env python
# coding: utf-8

# ## Importing required libraries

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


#accesing all required pickle files
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


# In[3]:


#storing all stopwords into dictionary for faster access
li=stopwords.words('english')
Stopwords={}
for i in li:
    Stopwords[i]=1


# In[4]:


#building vector for query that can used to find cosine similarity
def build_query_vector(words):
    vec=[]
    temp=0
    for w in words:
        tf_idf=(words.count(w)*math.log(len(file_with_index)/doc_fre[w]))
        vec.append(tf_idf)
        temp+=tf_idf**2
    q_norm=math.sqrt(temp)
    vec=np.array(vec)/q_norm
    return vec
#building vector for document i that can used to find cosine similarity
def build_d_vec(words,i):
    vec=[]
    for w in words:
        tf_idf=(doc_words[i].count(w)*math.log(len(file_with_index)/doc_fre[w]))
        vec.append(tf_idf)
    vec=np.array(vec)/doc_norm[i]
    return vec


# Here both documents are normalised and their dot product is considered.
# 
# i.e.$$cosine-sim(d1, d2)={\vec v (d1).\vec v (d2)}$$
# 
# $$cosine-sim(d1, d2)=\frac{\vec V (d1).\vec V (d2)}{|\vec V (d1)|.|\vec V (d2)|}$$
# 
# $\vec v (d1)$ and $\vec v (d2)$ are normalised document vectors.

# In[5]:


query=input("Enter your query")
#remove the punctuations
text = re.sub(r'[^\w\s]',' ',query)
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
tokenize_words=[word for word in tokenize_words if word not in Stopwords]
#remove all unnecessory words which not present in any dictionary
words=[word for word in tokenize_words if word in posting_list.keys()]

#building vector for query
q_vector=build_query_vector(words)

score={}
#proccessing for each document
for i in range(len(file_with_index)):
    #building vector for doc i
    d_vec=build_d_vec(words,i)
    #finding cosine simalarity for each doc and query vector
    score[i]=np.dot(q_vector,d_vec)#storing cosine similarity between doc i and query 

#sorting dictionary in desending order using score
score=sorted(score.items(),key=lambda x:x[1],reverse=True)


# In[6]:


#getting top 20 relevant document according to td_if score
count = 20
for i in score:
    if count == 0:
        break
    print(file_with_index[i[0]],i[1])
    count-=1


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




