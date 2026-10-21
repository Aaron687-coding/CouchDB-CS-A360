import couchdb
import mysql.connector
import time

import test_functions as tf

# FILL PASSWORDS IN
COUCH_DB_PASSWORD = "FILL ME IN"
MYSQL_PASSWORD = "FILL ME IN"

# PERFORMANCE TEST FUNC -- INITIALIZES, CALLS, ADDS, AND DELETES FUNCTIONS
# RESULTS RECORDED AND PRINTED IN TERMINAL
def performance_test():
    # ---------------- COUCHDB PERFORMANCE ----------------
    # Count time taken to initialize database
    s_time_init_c = time.perf_counter() # start time init couchdb
    db = tf.init_db_cdb(COUCH_DB_PASSWORD)
    e_time_init_c = time.perf_counter() # end time init couchdb

    # Count time taken to add 100 entries to database
    s_time_add_c = time.perf_counter()
    for i in range(100):
        tf.add_doc(db)
    e_time_add_c = time.perf_counter()

    # Count time taken to delete 100 entries from database (manually + bulk)
    # s_time_del_c_m = time.perf_counter() # ...delete couchdb manual

    # e_time_del_c_m = time.perf_counter()

    # Add 100 more values for bulk delete
    # for i in range(100):
    #     tf.add_doc(db)

    s_time_del_c_b = time.perf_counter() # ...delete couchdb bulk
    tf.delete_bulk_cdb(db)
    e_time_del_c_b = time.perf_counter()

    # Calculate everything and print
    d_time_init_c = e_time_init_c - s_time_init_c # Delta time init couchdb
    d_time_add_c = e_time_add_c - s_time_add_c
    d_time_del_c_b = e_time_del_c_b - s_time_del_c_b
    # d_time_del_c_m = e_time_del_c_m - s_time_del_c_m

    print("-------- CouchDB Performance Metrics --------\n" +
          f"\t- Create database in CouchDB:              {d_time_init_c} s\n" + 
          f"\t- Add 100 queries to database:             {d_time_add_c} s\n\n" +
          f"\t- Bulk delete 100 queries from database:   {d_time_del_c_b} s\n" +
          f"\t- Manual delete 100 queries from database:  N/A (Same as bulk)\n")


    # ----------------- MYSQL PERFORMANCE ------------------
    # Count the time taken to initialize database
    s_time_init_s = time.perf_counter() # Start time init SQL
    db_connection = tf.init_db_sql(MYSQL_PASSWORD)
    cursor = db_connection.cursor()
    e_time_init_s = time.perf_counter() # End time init SQL

    # Count the time taken to add 100 + 300 entries to the database (but in SQL)
    s_time_add_s = time.perf_counter()
    for i in range(100):
        tf.add_entry(cursor, i + 1) # Auto_increment PKs start from 1
    e_time_add_s = time.perf_counter()

    # Count the time taken to bulk delete both tables
    s_time_del_s_b = time.perf_counter()
    tf.delete_bulk_sql(cursor)
    e_time_del_s_b = time.perf_counter()

    # Add all entries back
    for i in range(100):
        tf.add_entry(cursor, i + 1) # Auto_increment PKs start from 1

    # Count the time taken to manually delete both tables
    s_time_del_s_m = time.perf_counter()
    for i in range(100):
        tf.delete_manual_sql(cursor, i + 1)
    e_time_del_s_m = time.perf_counter()

    # Calculate everything and print
    d_time_init_s = e_time_init_s - s_time_init_s # Delta time init couchdb
    d_time_add_s = e_time_add_s - s_time_add_s
    d_time_del_s_b = e_time_del_s_b - s_time_del_s_b
    d_time_del_s_m = e_time_del_s_m - s_time_del_s_m

    print("--------- MySQL Performance Metrics ---------\n" +
              f"\t- Create database in MySQL:                {d_time_init_s} s\n" + 
              f"\t- Add 100 queries to database:             {d_time_add_s} s\n\n" +
              f"\t- Bulk delete 100 queries from database:   {d_time_del_s_b} s\n" +
              f"\t- Manual delete 100 queries from database: {d_time_del_s_m}\n")
    
    # Statistics :D (compare both)
    print("--------- MySQL vs. CouchDB Performance Metrics  ---------\n" +
          f"\t- CouchDB was {100 * (d_time_init_s - d_time_init_c) / d_time_init_s}% faster than MySQL in initializing its database (and tables)\n" +
          f"\t- CouchDB was {100 * (d_time_add_s - d_time_add_c) / d_time_add_s}% faster than MySQL in creating documents\n" +
          f"\t- CouchDB was {100 * (d_time_del_s_b - d_time_del_c_b) / d_time_del_s_b}% faster than MySQL in bulk deleting documents")

    # Close the initial connection
    cursor.close()
    db_connection.close()

# TEST
if __name__ == "__main__":
    # Delete databases before performance test
    # db = tf.init_db_cdb()
    # db_connector = tf.init_db_sql()
    # cursor = tf.db_connector.cursor()



    performance_test()