# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

#import dependencies for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Import dependencies for Flask
from flask import Flask, jsonify

#Create first flask route
#@app.route('/')
#def hello_world():
#    return 'Hello world'

#Set up database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

#Save references 
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session link to our databases
session = Session(engine)

#Create flask app instance
app = Flask(__name__)

#Create Welcome Route
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    / api/v1.0/precipitation
    / api/v1.0/stations
    / api/v1.0/tobs
    / api/v1.0/temp/start/end
    ''')

#flask run
@app.route("/api/v1.0/precipitation")

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
#flask run

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

    if not end: 
        results = session.query(*sel).\
            filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
#flask run


if __name__=="__main__":
    app.run(debug=True)

