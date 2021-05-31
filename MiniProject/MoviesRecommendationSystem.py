'''for creating and accessing the structure and functions of the dataframe'''
import pandas as pd
'''for extracting keywords from the plot'''
from rake_nltk import Rake 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
'''CountVectorizer is needed to assign a numerical value to our bag of words string'''
from sklearn.feature_extraction.text import CountVectorizer

'''
json is needed to extract and clean the 
json data scraped from the URL of the open source movie database'''
import json

'''
urllib3 is needed to handle for the PoolManager() class which helps in handling details of 
connection pooling and thread safety
'''
import urllib3
    
    
def recommendations(title,val):
        
        
       df = pd.read_csv('bcd.csv')
       df = df[['Title','Genre','Director','Actors','Plot']]
    
        
       if val=='1':
            flag = 0
            for i in range(len(list(df['Title']))):
                if title==str(df['Title'][i]):
                           flag=1
            if flag == 0:
                   return -1
               
   
       for i in range(len(df.index)):
           gen=df['Genre'][i].lower().split(", ")
           df.at[i,'Genre']=gen
           dct=df['Director'][i].lower().split(" ")
           st=""
           for j in range(len(dct)):
               st=st+str(dct[j])
           df.at[i,'Director']=st
           act=df['Actors'][i].lower().split(", ")[:3]
           for j in range(len(act)):
               act[j]=act[j].replace(' ','')
           df.at[i,'Actors']=act

        
        
       
       df['Key_words'] = ""
    
       for index, row in df.iterrows():
            plot = row['Plot']
        
            """creating object of Rake class to extract keywords from plot"""
            r = Rake()
    
            """
            extract_keywords_from_plot function finds out the keywords from the passed
            string by removing common stop words like a,the,an,from,it..etc
            """
            r.extract_keywords_from_text(plot)
    
            """
            getting the dictionary of the extracted words where the words act as the
            keys and they have a numeric value assigned to them
            """
            key_words_dict_scores = r.get_word_degrees()
        
            """
            now we are assigning the list of the keywords from the dictionary to the
            newly created column called 'Key_words'
            """
            row['Key_words'] = list(key_words_dict_scores.keys())
       
    
       df['BOW']=""        
       df.drop(columns = ['Plot'], inplace = True)
        
        
       for i in range(len(df.index)):
                 s=""
                 lst=df['Genre'][i]
                 for j in range(len(lst)):
                       s=s+str(lst[j])+' '
                 s=s+str(df['Director'][0])
                 lst=df['Actors'][i]
                 for j in range(len(lst)):
                      s=s+str(lst[j])+' '
                 df.at[i,'BOW']=s
                 lst=df['Key_words'][i]
                 for j in range(len(lst)):
                      s=s+str(lst[j])+' '
                 df.at[i,'BOW']=s
        
       '''dropping every column except for bag_of_words as they are not needed anymore'''
       df.drop(columns = [col for col in df.columns if col!= 'BOW'], inplace = True)
       count = CountVectorizer()
       count_matrix = count.fit_transform(df['BOW'])
       #indices = pd.Series(df.index)
       cosine_sim = cosine_similarity(count_matrix, count_matrix)
       h=count_matrix.toarray()
       
       h=count_matrix.toarray()
       #Outermatrix=[]
       #print(h)
       for i in range(len(df.index)):
           var=h[0]
           j=0
           Innermatrix=[]
           for j in range(len(df.index)):
                    var2=h[j]
                    
                    numerator=0
                    denom1=0
                    denom2=0
                    
                    for o in range(len(h[0])):
                        numerator+=(var[o]*var2[o])
                        denom1+=(var[o]**2)
                        denom2+=(var2[o]**2)
                       
                    denom1=denom1**0.5
                    denom2=denom2**0.5
                    numerator=numerator/(denom1*denom2)
                    
                    Innermatrix.append(numerator)
                    
           print("COSINEFUNCTION\t \tMY LOOP\n")
           
           for k in range(0,5):         
               print(cosine_sim[0][k],"\t\t\t\t\t",Innermatrix[k])
           break
           #Outermatrix.append(Innermatrix)
           #break
               
        
           #print(Outermatrix)

recommendations('Fargo','0')

        

    
