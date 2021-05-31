# -*- coding: utf-8 -*-
"""
Created on Wed May 12 11:09:53 2021

@author: ACER
"""

import pandas as pd
'''for extracting keywords from the plot'''
from rake_nltk import Rake 

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
'''
df=pd.read_csv('bcd.csv')
df=df[['Title','Genre','Director','Actors','Plot']]
Movie='Moneyball'

y=recommendations(Movie,'1')
print(y)

values=''
if y==-1:
    url = "http://www.omdbapi.com/?i=tt3896198&apikey=7eaeeaff&t="+Movie
    http = urllib3.PoolManager()
    response = http.request('GET', url )
    data = response.data
    values = json.loads(data)
    if values['Response']=="True":
        tit=values['Title']
        gen=values['Genre']
        act=values['Actors']
        plt=values['Plot']
        dct=values['Director']
        s="N/A"
        if tit==s or act==s or gen==s or plt==s or dct==s:
            print("Sorry Not enough Data on this movie")
        else:
            df.loc[len(df.index)]=[tit,gen,dct,act,plt]
            df.to_csv('bcd.csv')
            messg=recommendations(Movie,'0')
            print("movie found")
    
'''








def func(t,g,d,a,p):
    df=pd.read_csv('bcd.csv')
    df=df[['Title','Genre','Director','Actors','Plot']]
    df.loc[len(df.index)]=[t,g,d,a,p]
    df.to_csv('bcd.csv',)
    '''
    entry={'Title':t,'Genre':g,'Director':d,'Actors':a,'Plot':p}
    df.append(entry,ignore_index=True)
    df.to_csv('bcd.csv',index=False)
    '''
    return
