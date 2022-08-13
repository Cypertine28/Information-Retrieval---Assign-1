CS657A: Information Retrieval
Assignment 1.

-------------------------------------
Name:Akash G. Panzade
Id:- 21111006
mail id:- akashp21@iitk.ac.in
-----------------------------

Dependencies:-
-------------
following packages or libraries to be installed to run assignment.
1.pandas
2.numpy
3.nltk
4.num2words
5.nltk.download('stopwords')
6.PorterStemmer

This directory contains following:
---------------------------------
i. Two zip files "21111006-qrels.zip" and "21111006-ir-systems.zip"
ii. Q1-preprocessing.py --- Q1 from assignment
			 --- this file contain preprocessing part , it much larger time on run and it produce .pkl file which can used further.
iii.Q2 ---This folder contain .py file for BRS,BM25,TF-IDF. We can run this file and give query an 
	  input and it print top 10 relevent documents. 
       ---to run :- $ python BM25py
       	    $ python BRS.py
       	    $ python TF-IDF.py
iv.pickle files --- data structures which store the data required to run the three systems.
v. makefile --- to run Q4 
vi.README file

Section A:- 
-----------
The "21111006-qrels.zip" file contains two files,
i. Queries.txt - this contain a set of 20 queries, each in one single line.The first field of a query line is the query id (from Q01 to Q20). The second field is a query text. The fields are separated by a TAB character.

ii. QRels.csv - It contains a set of 20 relevant documents for each query in the "Queries.txt" file in the following QRels format.
The column names are "QueryId", "Iteration", "DocId" and "Relevance".
"QueryId"   - represents the ID of the query.
"Iteration" - set to 1 by default.
"DocId"     - It is the ID of the document which is relevant to the given ""QueryId". This column contains for each query a set of 10 relevant documents in ranked order.
"Relevance" - it use to represent whether the document is relevant to the given query or not.1 for relevant to the given query and 0 otherwise.


Section B:-
-----------

This zip file contains the files asked in Q3.
The "21111006-ir-systems.zip" file contains the following files:
(1)BRS.py - contain code to implement simple Boolean Retrieval System.
(2)TF_IDF.py - contain code to implement a system from the TFIDF family.
(3)BM25.py - contain code to implement a system from the BM25 family.
(4)test.sh - this .sh file used in makefile to run all 3 systems.


Section C:- 
-----------
Makefile -- it invoking the "test.sh" file in the "21111006-ir-systems.zip" file and the query file is used as the parameter when running this Makefile .
How to run the Makefile:
------------------------
		At the time of running Makefile , user giver filename of input query file on which all 3 system run.
		For example, if the filename of the input query file is "query.txt", then we need to enter "query" (without quotes) in the Linux Terminal and then hit the enter key.
		e.g. $ make run filename=Queries

After running this Makefile it unzips the "21111006-ir-systems.zip" file and runs the "test.sh" file present in that file and all the three systems will run on given file and generate the outputs in CSV format in the same directory where this Makefile is present. The input query file should be present in the same directory where the Makefile is present.


i.  BRS.py generate "QRels_BRS.csv" 
ii. TFIDF.py generate "QRels_TF_IDF.csv" 
iii.BM25.py generate "QRels_BM25.csv"
Each of the output files will contain a set of 5 relevant documents for each query in the QRels format as given.
