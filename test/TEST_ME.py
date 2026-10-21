import couchdb
import mysql.connector
import time

import test_functions as tf

# FILL PASSWORDS IN
COUCH_DB_PASSWORD = "FILL ME IN"
MYSQL_PASSWORD = "FILL ME IN"

# Number of times to repeat the performance test; results are averaged at the end
NUM_RUNS = 5

# PERFORMANCE TEST FUNC -- INITIALIZES, CALLS, ADDS, AND DELETES FUNCTIONS
# RESULTS RECORDED AND PRINTED IN TERMINAL
# RETURNS a dict of all the measured delta times so results can be averaged across runs
def performance_test(run_number=None):
    run_label = f" (Run {run_number})" if run_number is not None else ""

    # Delete both databases first so we measure the actual cost of db creation
    tf.delete_db_cdb(COUCH_DB_PASSWORD)
    tf.delete_db_sql(MYSQL_PASSWORD)

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

    # Count time taken to delete 100 entries from database (bulk only)

    s_time_del_c_b = time.perf_counter() # ...delete couchdb bulk
    tf.delete_bulk_cdb(db)
    e_time_del_c_b = time.perf_counter()

    # Calculate everything and print
    d_time_init_c = e_time_init_c - s_time_init_c # Delta time init couchdb
    d_time_add_c = e_time_add_c - s_time_add_c
    d_time_del_c_b = e_time_del_c_b - s_time_del_c_b
    # d_time_del_c_m = e_time_del_c_m - s_time_del_c_m

    print(f"-------- CouchDB Performance Metrics{run_label} --------\n" +
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

    print(f"--------- MySQL Performance Metrics{run_label} ---------\n" +
          f"\t- Create database in MySQL:                {d_time_init_s} s\n" + 
          f"\t- Add 100 queries to database:             {d_time_add_s} s\n\n" +
          f"\t- Bulk delete 100 queries from database:   {d_time_del_s_b} s\n" +
          f"\t- Manual delete 100 queries from database: {d_time_del_s_m}\n")
    
    # Statistics :D (compare both)
    print(f"--------- MySQL vs. CouchDB Performance Metrics{run_label}  ---------\n" +
          f"\t- CouchDB was {100 * (d_time_init_s - d_time_init_c) / d_time_init_s}% faster than MySQL in initializing its database (and tables)\n" +
          f"\t- CouchDB was {100 * (d_time_add_s - d_time_add_c) / d_time_add_s}% faster than MySQL in creating documents\n" +
          f"\t- CouchDB was {100 * (d_time_del_s_b - d_time_del_c_b) / d_time_del_s_b}% faster than MySQL in bulk deleting documents\n")

    # Close the initial connection
    cursor.close()
    db_connection.close()

    # Return all measured delta times so they can be averaged across multiple runs
    return {
        "init_c": d_time_init_c,
        "add_c": d_time_add_c,
        "del_c_b": d_time_del_c_b,
        "init_s": d_time_init_s,
        "add_s": d_time_add_s,
        "del_s_b": d_time_del_s_b,
        "del_s_m": d_time_del_s_m,
    }

# Runs performance_test() NUM_RUNS times, printing results for each run, then
# calculates and prints the average of each measured metric across all runs
def run_multiple_tests(num_runs):
    all_results = []

    for run_number in range(1, num_runs + 1):
        print(f"\n=========== STARTING RUN {run_number} OF {num_runs} ===========\n")
        all_results.append(performance_test(run_number))

    # Average each metric across every run
    averages = {
        key: sum(result[key] for result in all_results) / num_runs
        for key in all_results[0]
    }

    print(f"\n=========== AVERAGE RESULTS ACROSS {num_runs} RUNS ===========\n")

    print("-------- CouchDB Average Performance Metrics --------\n" +
          f"\t- Create database in CouchDB:              {averages['init_c']} s\n" +
          f"\t- Add 100 queries to database:             {averages['add_c']} s\n\n" +
          f"\t- Bulk delete 100 queries from database:   {averages['del_c_b']} s\n" +
          f"\t- Manual delete 100 queries from database:  N/A (Same as bulk)\n")

    print("--------- MySQL Average Performance Metrics ---------\n" +
          f"\t- Create database in MySQL:                {averages['init_s']} s\n" +
          f"\t- Add 100 queries to database:             {averages['add_s']} s\n\n" +
          f"\t- Bulk delete 100 queries from database:   {averages['del_s_b']} s\n" +
          f"\t- Manual delete 100 queries from database: {averages['del_s_m']}\n")

    print("--------- MySQL vs. CouchDB Average Performance Metrics  ---------\n" +
          f"\t- CouchDB was {100 * (averages['init_s'] - averages['init_c']) / averages['init_s']}% faster than MySQL in initializing its database (and tables)\n" +
          f"\t- CouchDB was {100 * (averages['add_s'] - averages['add_c']) / averages['add_s']}% faster than MySQL in creating documents\n" +
          f"\t- CouchDB was {100 * (averages['del_s_b'] - averages['del_c_b']) / averages['del_s_b']}% faster than MySQL in bulk deleting documents\n")

# TEST
if __name__ == "__main__":
    run_multiple_tests(NUM_RUNS)