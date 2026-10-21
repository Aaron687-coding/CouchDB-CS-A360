# Our actual movie library

import couchdb
# from datetime import date

# import schemas # schemas.py -- contains class definitions of all "tables"

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
