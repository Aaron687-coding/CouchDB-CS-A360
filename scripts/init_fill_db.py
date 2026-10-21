# Our actual movie library

import couchdb
import json
import os

# import schemas # schemas.py -- contains class definitions of all "tables"

def init_db():
    couch = couchdb.Server('http://admin:[YOUR_PASSWORD]@localhost:5984/')

    db_name = 'csce-a360-moviedb'

    if db_name in couch:
        db = couch[db_name] # Select existing database
    else:
        db = couch.create(db_name) # Create new database

    return db

# TODO: Take all necessary values
#def fill_db(released, runtime, genre, plot, language, country, awards):
    # Continue along from here (shouldn't be that hard)

    # Not tricky with people, since there shouldn't be any duplicate
    # entries (either role or MovieID should be different)
#    return

def import_json_file_into_python():
    base_path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_path, 'movies', 'movies-250.json')
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def import_json_into_DB(db):
    data = import_json_file_into_python()
    
    if isinstance(data, dict) and 'docs' in data:
        data = data['docs']

    results = db.update(data)
    return


# Get the release date (e.g., "14 Oct 1994") of a movie and return a date structure
# def convert_date(str_date):
#    # Calculate the month number 
#    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#    month = months.index(str_date[3:6]) + 1

#    # Create a date object
#    movie_date = date(int(str_date[-4:]), month, int(str_date[:2]))
#    return movie_date
