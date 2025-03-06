import os
import flask
from flask import request, flash
import pandas as pd
import matplotlib.pyplot as plt

app = flask.Flask(__name__)

data = {'Nodarbība': ['6.12', '29.11', '22.11', '01.11'],
        'Atzīme': [4.92, 4.62, 4.76, 5.62]}
df = pd.DataFrame(data)
df.plot(x='Nodarbība', y='Atzīme', kind='bar', color='red')
plt.title('Atzīmes pa nodarbībām')
plt.savefig('static/myplot.png')



@app.route('/')
def home():
    return flask.render_template('home.html')


@app.route('/Upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return flask.render_template('upload.html')
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