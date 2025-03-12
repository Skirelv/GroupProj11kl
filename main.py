import os
import flask
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
table=df.to_html('templates/ExampTable.html')


@app.route('/')
def home():
    return flask.render_template('home.html')

@app.route('/Upload', methods=['GET', 'POST'])
def upload():
    return flask.render_template('upload.html')  

@app.route('/example')
def example():
    
    return flask.render_template('example.html')  

app.run()