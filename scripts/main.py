import init_fill_db

if __name__ == "__main__":
    testing = init_fill_db.init_db()

    init_fill_db.import_json_into_DB(testing)