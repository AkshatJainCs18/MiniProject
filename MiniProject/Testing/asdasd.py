        '''for creating and accessing the structure and functions of the dataframe'''
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
            
            
        def recommendations(title):
                
                df = pd.read_csv('C:/Users/ACER/Downloads/IMDBTOP250.csv')
        df = df[['Title','Genre','Director','Actors','Plot']]
        
        for i in range(250):
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
        
        for i in range(250):
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
            
        print(df['BOW'][0])
        df.drop(columns = [col for col in df.columns if col!= 'BOW'], inplace = True)
                count = CountVectorizer()
                count_matrix = count.fit_transform(df['BOW']
                indices = pd.Series(df.index)
            
            
                cosine_sim = cosine_similarity(count_matrix, count_matrix)
                recommended_movies = []
                
                # gettin the index of the movie that matches the title
                idx = indices[indices == title].index[0]
            
                # creating a Series with the similarity scores in descending order
                score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
            
                # getting the indexes of the 10 most similar movies
                top_10_indexes = list(score_series.iloc[1:11].index)
                
                # populating the list with the titles of the best 10 matching movies
                for i in top_10_indexes:
                    recommended_movies.append(list(df.index)[i])
              
                i=0
                lurl=list()
                while i<10:
                 movie=str(recommended_movies[i])
                 url = "http://www.omdbapi.com/?i=tt3896198&apikey=7eaeeaff&t="+movie
                 http = urllib3.PoolManager()
                 response = http.request('GET', url )
                 data = response.data
                 values = json.loads(data)
                 lurl.append(values['Poster'])
                 i=i+1
                print(recommended_movies)
                message = """<html>
                <head>
            <title>Recommended Movies</title>
            </head>
            <body>
            <table border='1'>
                    <tr><th>Title</th><th>Poster</th></tr>
                    <tr><td>"""+str(recommended_movies[0])+"""</td><td><img src="""+str(lurl[0])+"""></td></tr>
                    <tr><td>"""+str(recommended_movies[1])+"""</td><td><img src="""+str(lurl[1])+"""></td></tr>
                    <tr><td>"""+str(recommended_movies[2])+"""</td><td><img src="""+str(lurl[2])+"""></td></tr>
                    <tr><td>"""+str(recommended_movies[3])+"""</td><td><img src="""+str(lurl[3])+"""></td></tr>
                    <tr><td>"""+str(recommended_movies[4])+"""</td><td><img src="""+str(lurl[4])+"""></td></tr>
                    <tr><td>"""+str(recommended_movies[5])+"""</td><td><img src="""+str(lurl[5])+"""></td></tr>
                    <tr><td>"""+str(recommended_movies[6])+"""</td><td><img src="""+str(lurl[6])+"""></td></tr>
                    <tr><td>"""+str(recommended_movies[7])+"""</td><td><img src="""+str(lurl[7])+"""></td></tr>
                    <tr><td>"""+str(recommended_movies[8])+"""</td><td><img src="""+str(lurl[8])+"""></td></tr>
                    <tr><td>"""+str(recommended_movies[9])+"""</td><td><img src="""+str(lurl[9])+"""></td></tr>
            </table>
            </body>
        </html>>
           """  
                #return message
                
        recommendations('Fargo')
        
                
        
            
