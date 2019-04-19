# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 10:17:51 2019

@author: lorib
"""


# 1. import Flask
from flask import Flask

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
            f"Welcome to my 'Surfs Up! Homework' page!<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end><br/>")


# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")
    return "Welcome to my 'About' page!"


    return jsonify(precipitation)

Convert the query results to a Dictionary using date as the key and prcp as the value.
Return the JSON representation of your dictionary.

@app.route("/api/v1.0/justice-league/superhero/<superhero>")
def justice_league_character(superhero):
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""

    canonicalized = superhero.replace(" ", "").lower()
    for character in justice_league_members:
        search_term = character["superhero"].replace(" ", "").lower()

        if search_term == canonicalized:
            return jsonify(character)

    return jsonify({"error": f"Character with superhero {superhero} not found."}), 404


if __name__ == "__main__":
    app.run(debug=False)