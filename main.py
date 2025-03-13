import flask
from flask import request
import pandas as pd
from flask_peewee.db import Database
from peewee import FloatField, TextField 
import matplotlib.pyplot as plt

import os

DATABASE = {
    'name': 'data.db',
    'engine': 'peewee.SqliteDatabase'
}
SECRET_KEY = 'dingledong'

app = flask.Flask(__name__)
app.config.from_object(__name__)

db = Database(app)

class Data(db.Model):
    date = TextField()
    billsum = FloatField()

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
            for index, row in df.iterrows():
                Data.create(date=row['Month'], billsum=row['Amount'])

            return flask.render_template('view.html')
    return flask.render_template('upload.html')  


@app.route('/example')
def example():
    #data
    df = pd.read_csv('static/Example.csv', sep=';')
    #1st diagramm
    df.plot(x='Month', y='Amount', kind='bar', color='red')
    plt.title('Money spent')
    plt.legend().remove()
    plt.savefig('static/myplot1.png', dpi=75)
    #2nd diagramm
    labels=df['Month'].values
    df.plot.pie(y='Amount', labels=labels)
    plt.ylabel('')
    plt.title('Money spent')
    plt.legend().remove()
    plt.savefig('static/myplot2.png', dpi=75)
    #csv show 
    df.to_html('templates/examptable.html')

    return flask.render_template('example.html')  


if __name__ == '__main__':
    Data.create_table(fail_silently=True)
    app.run(debug=True)