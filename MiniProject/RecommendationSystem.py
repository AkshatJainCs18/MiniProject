"""
Project Number:17
Project Title:Recommendation System
(Movie Recommendation System)
Name:Akshat Jain
Section:A
Semester:6
Class Roll Number:12
BTech. CSE(Core)
UniVersity Roll Number:2013242
Admission Number:18141039
Email:asphalt51dc@gmail.com OR akshatjaincs18@gmail.com

"""
import pandas as pd
'''for extracting keywords from the plot'''
from rake_nltk import Rake 

"""cosine_similarity(..) function is used for calculating the similarity matrix from the sparse vectors"""
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


def rec(title,val):
    df = pd.read_csv('bcd.csv')
    df = df[['Title','Genre','Director','Actors','Plot']]
    #df.sort_values('Title',inplace=True)
    #df.drop_duplicates(subset='Title',keep='first',inplace=False)
    '''in case the movie is not found then -1 is returned to the function'''
    if val=='1':
          flag = 0
          for i in range(len(list(df['Title']))):
               if title==str(df['Title'][i]):
                       flag=1
          if flag == 0:
                   return -1
               
    '''cleaning the dataset'''
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
    
    '''following loop stores the extracted keywords from the 'Plot' column in a new column Key_words'''
    for i in range(len(df.index)):
            tempstr = str(df['Plot'][i])
             
            """creating object of Rake class to extract keywords from plot"""
            r = Rake()
    
            """
            extract_keywords_from_plot function finds out the keywords from the passed
            string by removing common stop words like a,the,an,from,it..etc
            """
            r.extract_keywords_from_text(tempstr)
    
            """
            getting the dictionary of the extracted words where the words act as the
            keys and they have a numeric value assigned to them
            """
            key_words = r.get_word_degrees()
            """
            now we are assigning the list of the keywords from the dictionary to the
            newly created column called 'Key_words'
            """
            df.at[i,'Key_words'] = list(key_words.keys())
            
    """Creating a new column for the concatenated strings to be stored as bag of words"""
    df['BOW']=""        
    df.drop(columns = ['Plot'], inplace = True)
    """The following loop creates the bag of strings for every row"""
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
    
    """Replacing the default indexing by the title of the movies"""
    df.set_index('Title', inplace = True)    
    
    """Dropping every column except for bag of words because they aren't needed beyond here"""
    df.drop(columns = [col for col in df.columns if col!= 'BOW'], inplace = True)
    
    """initializing an instance of CountVectorizer to create sparse matrix vectors"""
    count = CountVectorizer()
    count_matrix = count.fit_transform(df['BOW'])
    
    """calculating the similarity scores of the sparse matrix vectors and storing them in a 2d matrix"""
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    
    '''empty list to store the recommended movies'''
    rec_mov= []
    indexes=[]
    indices = pd.Series(df.index)
    '''idx stores the index of the movie input by the user'''
    idx = indices[indices == title].index[0]
    
    '''creating a series of scores of the movies corresponding to the input'''
    score = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    
    '''getting the indices of the top 10 closest related movies'''
    for i in range(1,11):
        indexes.append(score.index[i])
    
    '''Adding the recommended movies to the list '''
    for i in indexes:
            rec_mov.append(list(df.index)[i])

    i=0
    
    '''lurl is a list to store the url's of the posters of the movie'''
    lurl=list()
    '''year is a list to store the year of the release of the movie'''
    year=list()
    
    '''the following loop scrapes values of url and year from the open source movie database'''
    while i<10:
         movie=str(rec_mov[i])
         url = "http://www.omdbapi.com/?i=tt3896198&apikey=7eaeeaff&t="+movie
         http = urllib3.PoolManager()
         response = http.request('GET', url )
         data = response.data
         values = json.loads(data)
         lurl.append(values['Poster'])
         year.append(values['Year'])
         i=i+1
    '''css file for the output file'''
    css="""table{
    border-collapse: collapse;
    border:3px solid red;}
th{
    border:3px solid red;
    text-align:center;
    font-weight:bold;
    font-family:'Times New Roman', Times, serif;
    background-color:white;
    opacity:0.9;}
td{
    border:3px solid red;
    text-align:center;
    font-weight:bold;
    font-size:20px;
    font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    background-color:white;
    opacity:0.9;}"""


    message = """<html>
        <head>
    <title>Recommended Movies</title>
    <style>
     """+css+"""
    </style>
    </head>
    <body background="https://i.insider.com/5f578371e6ff30001d4e76be?width=1136&format=jpeg">
    <table border='1'>
    <tr><th>Title</th><th>Poster</th></tr>
    <tr><td>"""+str(rec_mov[0])+'<br>'+str(year[0])+"""</td><td><img src="""+str(lurl[0])+"""></td></tr>
    <tr><td>"""+str(rec_mov[1])+'<br>'+str(year[1])+"""</td><td><img src="""+str(lurl[1])+"""></td></tr>
    <tr><td>"""+str(rec_mov[2])+'<br>'+str(year[2])+"""</td><td><img src="""+str(lurl[2])+"""></td></tr>
    <tr><td>"""+str(rec_mov[3])+'<br>'+str(year[3])+"""</td><td><img src="""+str(lurl[3])+"""></td></tr>
    <tr><td>"""+str(rec_mov[4])+'<br>'+str(year[4])+"""</td><td><img src="""+str(lurl[4])+"""></td></tr>
    <tr><td>"""+str(rec_mov[5])+'<br>'+str(year[5])+"""</td><td><img src="""+str(lurl[5])+"""></td></tr>
    <tr><td>"""+str(rec_mov[6])+'<br>'+str(year[6])+"""</td><td><img src="""+str(lurl[6])+"""></td></tr>
    <tr><td>"""+str(rec_mov[7])+'<br>'+str(year[7])+"""</td><td><img src="""+str(lurl[7])+"""></td></tr>
    <tr><td>"""+str(rec_mov[8])+'<br>'+str(year[8])+"""</td><td><img src="""+str(lurl[8])+"""></td></tr>
    <tr><td>"""+str(rec_mov[9])+'<br>'+str(year[9])+"""</td><td><img src="""+str(lurl[9])+"""></td></tr>
    </table>
    </body>
    </html>>
   """  
    return message