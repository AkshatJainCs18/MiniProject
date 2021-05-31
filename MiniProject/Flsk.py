"""
Project Number:17
Project Title:Recommendation System
(Movie Recommendation System)
Name:Akshat Jain
Section:A
Class Roll Number:12
UniVersity Roll Number:2013242
Semester:6
BTech. CSE(Core)
Admission Number:18141039
Email:asphalt51dc@gmail.com OR akshatjaincs18@gmail.com
Semester:6
"""
'''Flask is used for handling the interaction between client and server'''
from flask import Flask,render_template,request,redirect,url_for
from RecommendationSystem import rec
import pandas as pd 

'''the CORS module is used to allow the server to send data which in turn permits the browser about
loading of resources'''
from flask_cors import CORS

'''json if used for handling the json files retrived from url while urllib is used to request for the file'''
import json
import urllib3

'''defines the root of the app'''
app= Flask(__name__,template_folder='template')
CORS(app)

'''default route '''
@app.route('/',methods = ['GET'])
def show_index_html():
    return render_template('index.html')

'''route for sending data to client side javascript as a JSON object'''
@app.route('/getdata',methods=['GET'])
def getdata():
    df = pd.read_csv('bcd.csv')
    lst=[]
    i=0
    while i < len(df.index):
        lst.append(df['Title'][i])
        i+=1
    return {"data":lst}
        

'''route for showing the output'''
@app.route('/RecommendedMovies', methods = ['POST'])
def get_data_from_html():
        Movie= request.form['Movie']
        y=rec(Movie,'1')
        messg=y
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
                pos=values['Poster']
                s="N/A"
                if tit==s or act==s or gen==s or plt ==s or dct==s or pos==s:
                    return redirect(url_for('not_enough_data'))
                else:
                    df=pd.read_csv('bcd.csv')
                    df=df[['Title','Genre','Director','Actors','Plot']]
                    df.loc[len(df.index)]=[tit,gen,dct,act,plt]
                    df.to_csv('bcd.csv')
                    return redirect(url_for('movie_added'))
                    
            else:
                return redirect(url_for('movie_doesnt_exist'))
        '''writing the contents received from RecommendationSystem.py on a new html file'''
        f = open('C:\\Users\\ACER\\Desktop\\MiniProject\\template\\output.html','w')
        f.write(messg)
        f.close()
        '''displaying the html file'''
        return render_template('output.html')

@app.route('/MovieDoesntExist')
def movie_doesnt_exist():
    return render_template('MovieDoesntExist.html')

@app.route('/NotEnoughData')
def not_enough_data():
    return render_template('NotEnoughData.html')

@app.route('/MovieAdded')
def movie_added():
    return render_template('index2.html')


if __name__=='__main__':
    '''allowing debugging in real time so that flask app doesnt need to be restarted every time to reflect
    change made by changing the code'''
    app.debug=True
    '''running the flask app on localhost'''
    app.run(host='127.0.0.1',port=5000)