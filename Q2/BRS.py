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


#accessing posting and file_with_index files 
temp=open('../pickle files/posting_list.pkl',"rb")
posting_lists=pickle.load(temp)

temp=open('../pickle files/files_with_index.pkl','rb')
file_index=pickle.load(temp)


# In[3]:


#getting all unique words
unique_words=set(posting_lists.keys())
# print(len(unique_words))


# In[4]:


### Store stopwords into dictioary for faster access
from nltk.corpus import stopwords
li=stopwords.words('english')
Stopwords={}
for i in li:
    Stopwords[i]=1

def numToWords(words):
    temp=[]
    for w in words:
        try:
            w=num2words(int(w))
        except:
            pass
        temp.append(w)
    return temp


# In[5]:


query=input("Enter your query")
#remove the punctuations
text = re.sub(r'[^\w\s]',' ',query)
# removing nonascii characters
encoded_string = text.encode("ascii", "ignore")
text = encoded_string.decode()
# tokenizing the doc texts
words=word_tokenize(text)
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
#remove all stopwords from query
word_list=[]
for w in words:
    if  (w not in Stopwords):
        word_list.append(w)
q_words=word_list
#print(q_words)


# In[6]:


#seperating each query word and adding "and" if there is no operator between words
li1=["and","or"]
for i in range(0,len(q_words)):
    if i==0:
        sep_words=[q_words[0]]
        continue
    if q_words[i] not in li1:
        if sep_words[-1] in li1:
            sep_words.append(q_words[i])
        else:
            sep_words.append("and")
            sep_words.append(q_words[i])
    elif sep_words[-1] not in li1:
        sep_words.append(q_words[i])
#print(sep_words)


# In[7]:


#this function help to sepeate operator and normal words used in query
def seperate(sep_words,op,normal_words):
    for i in sep_words:
        if i in li1:
            op.append(i)
        else:
            normal_words.append(i)
    return op,normal_words

op=[]
normal_words=[]
#getting seperated operator and normal words list
op,normal_words=seperate(sep_words,op,normal_words)
            
#print(op)
#print(normal_words)


# In[8]:


n=len(file_index)
#used 0for representing words not in that document and 1 for word present in that document ,this done for each query words 
def cons_vector(normal_words):
    vec_matrix1=[]
    for i in normal_words:
        #initizing with 0
        vec=[0]*n
        if i in unique_words:
            for j in posting_lists[i].keys():
                vec[j]=1 #update 0->1 for corresponding index which having that word using posting list
        vec_matrix1.append(vec)
    return vec_matrix1
vec_matrix=cons_vector(normal_words)


# In[9]:


#function helps to take "and"/"or" between generated vector list
def take_op(vector1,vector2,op):
    ans=[]
    for b1,b2 in zip(vector1,vector2):
        if op=="and":
            ans.append(b1&b2)
        else:
            ans.append(b1|b2)
    return ans
#iterating over all operators and performing boolean operation according to operator
for w in op:
    vector1=vec_matrix[0]
    vector2=vec_matrix[1]
    temp=take_op(vector1,vector2,w)
    #poping out 1st two used vector and adding result after performing boolean operation 
    vec_matrix.pop(0)
    vec_matrix.pop(0)
    vec_matrix.insert(0,temp)


# In[10]:


#getting all relevant file names
final_word_vector=vec_matrix[0]
cnt=0
files=[]
for i in final_word_vector:
    if i==1:
        files.append(file_index[cnt])
    cnt+=1


# In[11]:
p=10
for i in files:
    if(p==0):
        break
    p-=1
    print(i)


# In[ ]:





# In[ ]:





# In[ ]:




