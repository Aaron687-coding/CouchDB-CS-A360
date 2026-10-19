import couchdb
import mysql.connector
import time
from datetime import date

import schemas # schemas.py -- contains class definitions of all "tables"

def add_doc(db):
    doc = {"Name": "Guido", "Favorite food": ["Apple", "Pear", "Orange"], "Age": 20 }

    db.save(doc)

def add_entry(cursor, id):
    cursor.execute("INSERT INTO test "
                   "(PersonID, Name, Age)"
                    f"VALUES ({id}, 'Guido', 20)")

    food = ["Apple", "Pear", "Orange"]
    for j in range(3):
        cursor.execute("INSERT INTO favorite_food "
                       "(PersonID, Food)"
                       f"VALUES ({id}, {food[j]})")

def init_db():
    couch = couchdb.Server('http://admin:couchPouch1241^v@localhost:5984/')

    db_name = 'csce-a360-moviedb'

    if db_name in couch:
        db = couch[db_name] # Select existing database
    else:
        db = couch.create(db_name) # Create new database
    
    return db

# TEST
if __name__ == "__main__":
    db = init_db()

    start_time = time.perf_counter()

    for i in range(100):
        add_doc(db)
    
    end_time = time.perf_counter()

    delta_time = end_time - start_time

    print(delta_time)

    # 1. Connect to the MySQL Server
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",        # Replace with your MySQL username
        password="Rootbeer543!"  # Replace with your MySQL password
    )

    cursor = db_connection.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS csceA360Test") # No dashes
    cursor.execute("USE csceA360Test")
    # cursor.execute("CREATE TABLE test (PersonID Int PRIMARY KEY UNIQUE AUTO_INCREMENT NOT NULL, Name VARCHAR(30) NOT NULL, Age Int)")
    # cursor.execute("CREATE TABLE favorite_food (PersonID Int NOT NULL, Food VARCHAR(30) NOT NULL, FOREIGN KEY (PersonID) REFERENCES test(PersonID))")

    start_time_sql = time.perf_counter()

    for i in range(100):
        add_entry(cursor, i)
    
    end_time_sql = time.perf_counter()

    delta_time_sql = end_time_sql - start_time_sql

    print("\n" + str(delta_time_sql))

    # Close the initial connection
    cursor.close()
    db_connection.close()

# TODO: Take all necessary values
def fill_db(released, runtime, genre, plot, language, country, awards):
    # Continue along from here (shouldn't be that hard)

    # Not tricky with people, since there shouldn't be any duplicate
    # entries (either role or MovieID should be different)
    return

# Get the release date (e.g., "14 Oct 1994") of a movie and return a date structure
def convert_date(str_date):
    # Calculate the month number 
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month = months.index(str_date[3:6]) + 1

    # Create a date object
    movie_date = date(int(str_date[-4:]), month, int(str_date[:2]))
    return movie_date
