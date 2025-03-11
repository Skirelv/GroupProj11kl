import os
import flask
from flask import request, flash
import pandas as pd
from flask_peewee.db import Database
import matplotlib.pyplot as plt

app = flask.Flask(__name__)

DATABASE = {
    'name': 'stats.db',
    'engine': 'peewee.SqliteDatabase'
}
app.secret_key = 'dingledong'

#data
df = pd.read_csv('static/Example.csv', sep=';')
#1st diagramm
df.plot(x='Month', y='Amount', kind='bar', color='red')
plt.title('Atzīmes pa nodarbībām')
plt.legend().remove()
plt.savefig('static/myplot1.png')
#2nd diagramm
labels=df['Month'].values
df.plot.pie(y='Amount', labels=labels)
plt.title('Atzīmes pa nodarbībām')
plt.legend().remove()
plt.savefig('static/myplot2.png')


@app.route('/')
def home():
    return flask.render_template('home.html')


@app.route('/Upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
        if file.filename.endswith('.csv') == False:
            flash('Not a csv file')
    return flask.render_template('upload.html')  

@app.route('/example')
def example():
    return flask.render_template('example.html')  

app.run()