from flask import Flask,render_template,request
from MoviesRecommendationSystem import recommendations
#from RecommendationSystem import rec
import pandas as pd 
from flask_cors import CORS
import json
import urllib3
from fiddlingwithcsv import func

app= Flask(__name__,template_folder='template')
CORS(app)

@app.route('/',methods = ['GET'])
def show_index_html():
    return render_template('index.html')


@app.route('/getdata',methods=['GET'])
def getdata():
    df = pd.read_csv('bcd.csv')
    lst=[]
    i=0
    while i < len(df.index):
        lst.append(df['Title'][i])
        i+=1
    return {"data":lst}
        


@app.route('/RecommendedMovies', methods = ['POST'])
def get_data_from_html():
        
        
        Movie= request.form['Movie']
        y=recommendations(Movie,'1')
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
                    return render_template('NotEnoughData.html')
                else:
                    func(tit,gen,dct,act,plt)
                    messg=recommendations(Movie,'0')
            else:
                return render_template('MovieDoesntExist.html')
        f = open('C:\\Users\\ACER\\Desktop\\MiniProject\\template\\output.html','w')
        f.write(messg)
        f.close()
        return render_template('output.html')

if __name__=='__main__':
    app.debug=True
    app.run(host='127.0.0.1',port=5000)