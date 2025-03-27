# Import required libraries
import flask
from flask import request
import pandas as pd
from flask_peewee.db import Database
from peewee import FloatField, TextField, IntegerField
import matplotlib
matplotlib.use('Agg')  # Configure matplotlib to work in non-interactive mode (backend only)
import matplotlib.pyplot as plt

# Database configuration
DATABASE = {
    'name': 'data.db',
    'engine': 'peewee.SqliteDatabase'
}
SECRET_KEY = 'dingledong'

# Initialize Flask application
app = flask.Flask(__name__)
app.config.from_object(__name__)

# Initialize database
db = Database(app)

# Define database model
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
            # Read CSV file with semicolon separator
            df = pd.read_csv(file, sep=';')
            # Clear existing data
            Data.delete().execute()
            # Insert new data from CSV
            for index, row in df.iterrows():
                Data.create(Year=row['Year'], 
                            Month=row['Month'], 
                            Electricity=float(row['Electricity']), 
                            Water=float(row['Water']), 
                            Gas=float(row['Gas']), 
                            Internet=float(row['Internet']), 
                            Sum=float(row['Sum']))
            df.to_html('templates/viewtable.html')
            return flask.render_template('upload.html')  
    return flask.render_template('upload.html')  

# Route for data visualization
@app.route('/view', methods=['GET','POST'])
def view():
    # Get unique years and months from database for dropdown menus
    Years_list=Data.select(Data.Year).distinct()
    Month_list=Data.select(Data.Month).distinct()
    
    # Check if there's any data in the database
    has_data = Data.select().count() > 0
    
    if request.method == 'POST':
        choices = request.form
        # Handle different types of data visualization requests
        if choices['DataType'] == '1YearAllMonth1Data':
            # Get data for one bill type across all months in a year
            Bill = choices['Bill']
            Colx = Data.select(getattr(Data, Bill)).where(Data.Year == choices['Year']) 
            Coly = Data.select(Data.Month).where(Data.Year == choices['Year'])
            xlist = [getattr(row, Bill) for row in Colx]
            ylist = [row.Month for row in Coly]
            title = 'How much money was spent on ' + choices['Bill'] + ' in the year ' + choices['Year']
        else:
            # Get data for all bill types in a specific month and year
            Col = Data.get_or_none((Data.Year == choices['Year']) & (Data.Month == choices['Month']))
            xlist = [Col.Electricity, Col.Water, Col.Gas, Col.Internet]
            ylist = ['Electricity', 'Water', 'Gas', 'Internet']
            title = 'How much money was spent in ' + choices['Year'] + ' ' + choices['Month']
        
        # Create new figure with specified size
        plt.figure(figsize=(10, 6))
        
        # Generate appropriate chart based on user selection
        if choices['ChartType'] == 'Histogram':
            # Create bar chart
            plt.bar(x=ylist, height=xlist)
            plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
            plt.title(title, pad=20)  
            plt.tight_layout()
        else:
            # Create pie chart
            plt.pie(x=xlist, labels=ylist, autopct='%1.1f%%', pctdistance=0.85)
            plt.title(title, pad=20) 
            plt.tight_layout() 
                
        # Save the plot and clean up
        plt.savefig('static/dataplot.png', bbox_inches='tight', dpi=75)
        plt.close('all')
        return flask.render_template('view.html', years=Years_list, months=Month_list, has_data=has_data)
    return flask.render_template('view.html', years=Years_list, months=Month_list, has_data=has_data)

@app.route('/example')
def example():
    # Read example data from CSV
    df = pd.read_csv('static/Example.csv', sep=';')
    
    # Create first diagram (bar chart)
    monthlist = df[df['Year'] == 2021]['Month']
    electricity_2021 = df[df['Year'] == 2021]['Electricity']
    print(electricity_2021)
    
    plt.figure(figsize=(10, 6))
    plt.bar(height=electricity_2021, x=monthlist)
    plt.xticks(rotation=45, ha='right')
    plt.title('How much money was spent on electricity in the year 2021', pad=20)
    plt.tight_layout()
    plt.savefig('static/myplot1.png', bbox_inches='tight', dpi=75)
    plt.close('all')
    
    # Create second diagram (pie chart)
    plt.figure(figsize=(10, 6))
    plt.pie(x=electricity_2021, labels=monthlist, autopct='%1.1f%%', pctdistance=0.85)
    plt.title('How much money was spent on electricity in the year 2021', pad=20)
    plt.tight_layout()
    plt.savefig('static/myplot2.png', bbox_inches='tight', dpi=75)
    plt.close('all')
    
    # Convert DataFrame to HTML for display
    df.to_html('templates/examptable.html')

    return flask.render_template('example.html')  

# Initialize database and run the application
if __name__ == '__main__':
    # Clear data from database
    Data.delete().execute()
    # Create table if it doesn't exist
    Data.create_table(fail_silently=True)
    # Run the Flask application in debug mode
    app.run(debug=True)