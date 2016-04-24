from flask import *
from flask import g
import sqlite3

from bike_scraper.core import *
from bike_scraper.json_generator import *
from bike_scraper.averages import *

app = Flask(__name__)

#Declaratin of our objects and database directory
DATABASE = 'data/bikedata.db'
jsonFetcher = json_generator()
scraper = BikeScraper()
ave = averager()

def connect_to_database():
    '''Connect to the SQLite database whose path is assigned to the DATABASE variable'''
    return sqlite3.connect(DATABASE)

def get_db():
    '''Returns the database as a variable'''
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    '''Closes connection to database on teardown (when query is finished)'''
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/getjson/<sid>/<day>')
def jsonstuff(sid, day):
    '''This is the main querying function for the flask application. It takes in the station ID an day of the week to be queried from the javascript
    file and then uses the averager object to find and return historical data information in JSON format to be displayed on the website.'''
    
    cur = get_db().cursor()
    hourly = ave.getHourAverage(cur, sid, day) #Returns a list containing the hourly average available bikes from 6am to midnight
    daily = ave.getDayAverage(cur, sid) #returns the daily average available bikes for each day of the week
    free_time = ave.calculate_freetime(cur, sid, day) #returns the average waiting time for an available bike for a particular day in 3 hour blocks
    jsonFile = jsonFetcher.generate_json(hourly, daily, free_time) #Combines thos three lists into a single JSON file
    return jsonFile
    

@app.route('/')
def homePage():
    '''This is a simple function that renders the main html file when the homepage is queried'''
    return render_template('bikemap.html')

if __name__ == '__main__':
    app.run(debug = True)