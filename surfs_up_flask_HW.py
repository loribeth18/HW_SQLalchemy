# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 19:49:37 2019

@author: lorib
"""

# 1. import Flask
from flask import Flask, jsonify

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


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
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    order_by(Measurement.date).all()
   d = {date: prcp for (date, prcp) in precipitation}
   return jsonify(d)


@app.route("/api/v1.0/stations")
def stations():
   active_stations=session.query(Station.station, Station.name).\
    order_by(Station.station).desc().all()
   s = {station: name for (station, name) in active_stations}
   return jsonify(s)

@app.route("/api/v1.0/tobs")
def tobs():
   tob = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()
   t = {date: prcp for (date, prcp) in tob}
   return jsonify(t)


@app.route("/api/v1.0/<start>")
def start(start_date):
    canonicalized = date.replace(" ", "").lower()
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()



@app.route("/api/v1.0/<start>/<end>")
def trip_calc_temps(start_date, end_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        
        

if __name__ == "__main__":
    app.run(debug=False)