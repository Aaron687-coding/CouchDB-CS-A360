from pydantic import BaseModel, Field
from dataclasses import dataclass
from datetime import date
from typing import Optional

# Raters we have:
# - Internet Movie Database (IMDB) - Value, imdbRating, imdbVotes, imdbID
# - Rotten Tomatoes - Value
# - Metacritic - Value, Metascore

# Create ratings subschema (i.e., struct)
@dataclass
class Rating:
    Source: str
    Value: int

# Create movie schema 
class movieSchema(BaseModel):
    doc_type: str = "movie"
    
    MovieID: str
    Released: Optional[date] = None # default to empty date
    Runtime: int

    Genre: str # Contains multiple genres separated by commas (", ")
    Plot: str
    Language: str
    Country: str
    Awards: str # "Nominated for ...", "Won ..."

    Ratings: list[Rating] # IMDB, Rotten Tomatoes, Metacritic
    imdbRating: int
    imdbVotes: int
    imdbID: int
    Metascore: int
    # Type: str # Added just in case; remove if not needed
    BoxOffice: int # Money made

# Create people schema ((MovieID, (LastName, FirstName)) -> Role
class personSchema(BaseModel):
    doc_type: str = "person"

    MovieID: str # FK to referencing movie
    LastName: str
    FirstName: str
    Role: str # Writer, Director, Actor