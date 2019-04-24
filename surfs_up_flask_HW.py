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
   session = Session(engine)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    order_by(Measurement.date).all()
   d = {date: prcp for (date, prcp) in precipitation}
   return jsonify(d)


@app.route("/api/v1.0/stations")
def stations():
   session = Session(engine)
   active_stations=session.query(Station.station, Station.name).\
    order_by(Station.station.desc()).all()
   s = {station: name for (station, name) in active_stations}
   return jsonify(s)

@app.route("/api/v1.0/tobs")
def tobs():
   session = Session(engine)
   tob = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()
   t = {date: tobs for (date, tobs) in tob}
   return jsonify(t)


@app.route("/api/v1.0/<start_date>")
def start(start_date=None):
    session = Session(engine)
    trip_start= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    ts = list(np.ravel(trip_start))
    return jsonify(ts)



@app.route("/api/v1.0/<start_date>/<end_date>")
def trip_calc_temps(start_date, end_date):
    session = Session(engine)
    trip_start_end= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    tse = list(np.ravel(trip_start_end))    
    return jsonify(tse)
    

if __name__ == "__main__":
    app.run(debug=False)