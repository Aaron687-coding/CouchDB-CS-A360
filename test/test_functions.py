import couchdb
import mysql.connector
import time

# Initializes (or selects) couchdb db
def init_db_cdb(password):
    couch = couchdb.Server(f'http://admin:{password}@localhost:5984/')

    db_name = 'csce-a360-test'

    if db_name in couch:
        db = couch[db_name] # Select existing database
    else:
        db = couch.create(db_name) # Create new database
    
    return db

# Initializes (and selects) MySQL db
def init_db_sql(password):
    # Connect to the MySQL Server
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        autocommit=True # To ensure that transactions managed to be complete before
                        # The connection gets closed (previously INSERT/DELETE commands 
                        # Would be silently rolled back, causing leftover entries)
    )

    cursor = db_connection.cursor()

    cursor.execute( "CREATE DATABASE IF NOT EXISTS csceA360Test") # No dashes
    cursor.execute( "USE csceA360Test") # Use said database, and create its tables

    cursor.execute( "CREATE TABLE IF NOT EXISTS PERSON "
                    "(PersonID Int PRIMARY KEY UNIQUE AUTO_INCREMENT NOT NULL, "
                    "Name VARCHAR(30) NOT NULL, "
                    "Age Int)")
    
    cursor.execute( "CREATE TABLE IF NOT EXISTS FAVORITE_FOOD "
                    "(FoodID Int PRIMARY KEY UNIQUE AUTO_INCREMENT NOT NULL, "
                    "PersonID Int NOT NULL, "
                    "Food VARCHAR(30) NOT NULL, "
                        "CONSTRAINT Fav_Food_PersonID_FK FOREIGN KEY (PersonID) REFERENCES PERSON(PersonID))")

    return db_connection

# Deletes couchdb db entirely (for it to be created in performance_test())
def delete_db_cdb(password):
    couch = couchdb.Server(f'http://admin:{password}@localhost:5984/')

    db_name = 'csce-a360-test'

    if db_name in couch:
        del couch[db_name]

# Deletes MySQL db entirely (for it to be created in performance_test())
def delete_db_sql(password):
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        autocommit=True
    )

    cursor = db_connection.cursor()
    cursor.execute("DROP DATABASE IF EXISTS csceA360Test")

    cursor.close()
    db_connection.close()

# CouchDB document adder func
def add_doc(db):
    doc = {"Name": "Guido", "Favorite food": ["Apple", "Pear", "Orange"], "Age": 20 }

    db.save(doc)

# SQL entry adder func 
def add_entry(cursor, id):
    cursor.execute(  "INSERT INTO PERSON (PersonID, Name, Age)"
                    f"VALUES ({id}, 'Guido', 20)")

    food = ["Apple", "Pear", "Orange"]
    for j in range(3):
        cursor.execute(  "INSERT INTO FAVORITE_FOOD (FoodID, PersonID, Food)"
                        f"VALUES (NULL, {id}, '{food[j]}')") # auto_increment sees null and replaces it

# Couchdb bulk delete func
def delete_bulk_cdb(db):
    docs_to_delete = []

    # Use "_all_docs" endpoint to get ALL docs in db
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

    # Execute the bulk deletion
    if docs_to_delete:
        db.update(docs_to_delete)
    
    # What we did above wasn't deleting, but append a change to them (called metadata)!
    # (They are now tombstones)
    # As metadata steadily increases, data consumption increases, since each change is 
    # Appended to the original doc instead of modifying the original (this helps when the db crashes); 
    # To actually apply these changes, we call:
    # db.compact()

# Couchdb manual delete func
# Uhh it doesn't look like there is one 
# (there's either using curl or setting deleted to true, like above)
def delete_manual_cdb(db):
    return

# MySQL bulk delete (just truncate the tables)
def delete_bulk_sql(cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("TRUNCATE TABLE PERSON")
    cursor.execute("TRUNCATE TABLE FAVORITE_FOOD")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# MySQL manual delete func
def delete_manual_sql(cursor, id):
    # Delete the FAVORITE_FOOD rows first to avoid the foreign constraint from
    # Triggering an error (referencing a Person that doesn't exist)
    for i in range(3):
        cursor.execute(f"DELETE FROM FAVORITE_FOOD WHERE FoodID = {3 * (id - 1) + i + 1}")
    cursor.execute(f"DELETE FROM PERSON WHERE PersonID = {id}")