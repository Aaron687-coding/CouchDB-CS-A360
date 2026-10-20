import couchdb
import mysql.connector
import time
from datetime import date

# import schemas # schemas.py -- contains class definitions of all "tables"

def init_db_cdb():
    couch = couchdb.Server('http://admin:couchPouch1241^v@localhost:5984/')

    db_name = 'csce-a360-moviedb'

    if db_name in couch:
        db = couch[db_name] # Select existing database
    else:
        db = couch.create(db_name) # Create new database
    
    return db

def init_db_sql():
    # 1. Connect to the MySQL Server
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rootbeer543!"
    )

    cursor = db_connection.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS csceA360Test") # No dashes
    cursor.execute("USE csceA360Test") # Use said database, and create its tables
    cursor.execute("CREATE IGNORE TABLE TEST (PersonID Int PRIMARY KEY UNIQUE AUTO_INCREMENT NOT NULL, Name VARCHAR(30) NOT NULL, Age Int)")
    cursor.execute("CREATE IGNORE TABLE FAVORITE_FOOD (PersonID Int NOT NULL, Food VARCHAR(30) NOT NULL, FOREIGN KEY (PersonID) REFERENCES TEST(PersonID))")

    return db_connection.cursor()

# CouchDB document adder func
def add_doc(db):
    doc = {"Name": "Guido", "Favorite food": ["Apple", "Pear", "Orange"], "Age": 20 }

    db.save(doc)

# SQL entry adder func 
def add_entry(cursor, id):
    cursor.execute("INSERT INTO TEST (PersonID, Name, Age)"
                  f"VALUES ({id}, 'Guido', 20)")

    food = ["Apple", "Pear", "Orange"]
    for j in range(3):
        cursor.execute("INSERT INTO FAVORITE_FOOD (PersonID, Food)"
                      f"VALUES ({id}, {food[j]})")

def delete_bulk_cdb(db):
    docs_to_delete = []

    # Use _all_docs endpoint to get ALL docs in db
    for row in db.view("_all_docs"):
        doc_id = row.id
        # Skip design documents (views, validation, updates, filters)
        if doc_id.startswith("_design/"):
            continue
            
        # Fetch the minimal info needed: ID and current Revision
        docs_to_delete.append({
            "_id": doc_id,
            "_rev": row.value["rev"],
            "_deleted": True  # Flag that tells couchdb to delete this doc
        })

    # 2. Execute the bulk deletion
    if docs_to_delete:
        db.update(docs_to_delete)

def main():
    # Delete couchdb database and SQL database

    # ---------------- COUCHDB PERFORMANCE ----------------
    # Count time taken to initialize database
    s_time_init_c = time.perf_counter() # start time init couchdb
    db = init_db_cdb()
    e_time_init_c = time.perf_counter() # end time init couchdb

    # Count time taken to add 100 entries to database
    s_time_add_c = time.perf_counter()
    for i in range(100):
        add_doc(db)
    e_time_add_c = time.perf_counter()

    # Count time taken to delete 100 entries from database (manually + bulk)
    s_time_del_c_m = time.perf_counter() # ...delete couchdb manual
    delete_bulk_cdb(db)
    e_time_del_c_m = time.perf_counter()

    # Add 100 more values for bulk delete
    for i in range(100):
        add_doc(db)

    s_time_del_c_b = time.perf_counter() # ...delete couchdb bulk

    e_time_del_c_b = time.perf_counter()

    # Calculate everything and print
    d_time_init_c = e_time_init_c - s_time_init_c
    d_time_add_c = e_time_add_c - s_time_add_c
    d_time_del_c = e_time_del_c - s_time_del_c

    print("-------- CouchDB Performance Metrics --------\n" +
          f"\t- Create database in CouchDB:        {d_time_init_c} s\n" + 
          f"\t- Add 100 queries to database:       {d_time_add_c} s\n" +
          f"\t- Delete 100 queries from database:  {d_time_del_c} s\n")


    # ----------------- MYSQL PERFORMANCE ------------------
    # Count the time taken to initialize database
    s_time_init_s = time.perf_counter() # Start time init SQL
    cursor = init_db_sql()
    e_time_init_s = time.perf_counter() # End time init SQL

    # Count the time taken to add 100 entries to the database (but in SQL)
    s_time_add_s = time.perf_counter()
    for i in range(100):
        add_entry(cursor, i)
    e_time_add_s = time.perf_counter()

    delta_time_sql = end_time_sql - start_time_sql

    print("\n" + str(delta_time_sql))

    # Close the initial connection
    cursor.close()
    db_connection.close()

# TEST
if __name__ == "__main__":
    main()


# --------- BELOW IS NOT RELEVANT FOR TEST ----------

# TODO: Take all necessary values
#def fill_db(released, runtime, genre, plot, language, country, awards):
    # Continue along from here (shouldn't be that hard)

    # Not tricky with people, since there shouldn't be any duplicate
    # entries (either role or MovieID should be different)
#    return

# Get the release date (e.g., "14 Oct 1994") of a movie and return a date structure
# def convert_date(str_date):
#    # Calculate the month number 
#    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#    month = months.index(str_date[3:6]) + 1

#    # Create a date object
#    movie_date = date(int(str_date[-4:]), month, int(str_date[:2]))
#    return movie_date
