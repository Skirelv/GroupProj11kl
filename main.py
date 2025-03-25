import flask
from flask import request
import pandas as pd
from flask_peewee.db import Database
from peewee import FloatField, TextField, IntegerField
import matplotlib
matplotlib.use('Agg') # makes plots only on the backend
import matplotlib.pyplot as plt

DATABASE = {
    'name': 'data.db',
    'engine': 'peewee.SqliteDatabase'
}
SECRET_KEY = 'dingledong'

app = flask.Flask(__name__)
app.config.from_object(__name__)

db = Database(app)

class Data(db.Model):
    Year = IntegerField()
    Month = TextField()
    Electricity = FloatField()
    Water = FloatField()
    Gas = FloatField()
    Internet = FloatField()
    Sum = FloatField()

@app.route('/')
def home():
    return flask.render_template('home.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST': 
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file'] 
        if file:
            df = pd.read_csv(file, sep=';')
            Data.delete().execute()
            for index, row in df.iterrows():
                Data.create(Year=row['Year'], 
                            Month=row['Month'], 
                            Electricity=float(row['Electricity']), 
                            Water=float(row['Water']), 
                            Gas=float(row['Gas']), 
                            Internet=float(row['Internet']), 
                            Sum=float(row['Sum']))
            return flask.render_template('upload.html')  
    return flask.render_template('upload.html')  



@app.route('/view', methods=['GET','POST'])
def view():
    Years_list=Data.select(Data.Year).distinct()
    Month_list=Data.select(Data.Month).distinct()
    if request.method == 'POST':
        choices = request.form
        #get lists from database
        if choices['DataType'] == '1YearAllMonth1Data':
            Bill = choices['Bill']
            Colx = Data.select(getattr(Data, Bill)).where(Data.Year == choices['Year']) 
            Coly = Data.select(Data.Month).where(Data.Year == choices['Year'])
            xlist = [getattr(row, Bill) for row in Colx]
            ylist = [row.Month for row in Coly]
            plt.title('How much money was spent on ' + choices['Bill'] + ' in the year ' + choices['Year'])
        else:
            Col = Data.get_or_none((Data.Year == choices['Year']) & (Data.Month == choices['Month']))
            xlist = [Col.Electricity, Col.Water, Col.Gas, Col.Internet]
            ylist = ['Electricity', 'Water', 'Gas', 'Internet']
            plt.title('How much money was spent in ' + choices['Year'] + ' ' + choices['Month'])
        #make the diagrammes
        if choices['ChartType'] == 'Histogram':
                plt.bar(x=ylist, height=xlist)
                plt.legend().remove()
        else:
                plt.pie(x=xlist,labels=ylist)
                plt.legend().remove()
                
        #save the diagramme
        plt.savefig('static/dataplot.png')
        plt.close('all')
        return flask.render_template('view.html', years=Years_list, months=Month_list)
    return flask.render_template('view.html', years=Years_list, months=Month_list)


@app.route('/example')
def example():
    #data
    df = pd.read_csv('static/Example.csv', sep=';')
    #1st diagramm
    monthlist = df[df['Year'] == 2021]['Month']
    electricity_2021 = df[df['Year'] == 2021]['Electricity']
    print(electricity_2021)
    plt.bar(height=electricity_2021, x=monthlist)
    plt.legend().remove()
    plt.title('How much money was spent on electricity in the year 2021')
    plt.savefig('static/myplot1.png', dpi=75)
    plt.close('all')
    #2nd diagramm
    plt.pie(x=electricity_2021, labels=monthlist)
    plt.legend().remove()
    plt.title('How much money was spent on electricity in the year 2021')
    plt.savefig('static/myplot2.png', dpi=75)
    plt.close('all')
    #csv show 
    df.to_html('templates/examptable.html')

    return flask.render_template('example.html')  


if __name__ == '__main__':
    Data.create_table(fail_silently=True)
    app.run(debug=True)