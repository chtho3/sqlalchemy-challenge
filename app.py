from flask import Flask, jsonify

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


@app.route("/")
def home():
    return(
     "Please navigate to one of the following API pages: </br>"
     "/api/v1.0/precipitation </br>"
     "/api/v1.0/stations </br>"
     "/api/v1.0/tobs </br>"
     "/api/v1.0/<start> and /api/v1.0/<start>/<end>"
     )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    prcp_query = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    
    prcp_list = []
    for date, prcp in prcp_query:
        prcp_dict={}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        prcp_list.append(prcp_dict)
        
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_data = session.query(Station.station).all()
    session.close()
    
    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def temps():
    session = Session(engine)
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-23").all()
    session.close()
    
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def date_start(start = None):
    session = Session(engine)
    start_date = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
        
    session.close()
    
    return jsonify(start_date)
    return f"Start Date not found.", 404

@app.route("/api/v1.0/<start>/<end>")
def date_btwn(start = None, end = None):
    
    session = Session(engine)
    btwn_date = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        
    session.close()
    
    return jsonify(btwn_date)
    return f"Date range not found.", 404

if __name__ == "__main__":
    # @TODO: Create your app.run statement here
    # YOUR CODE GOES HERE
    app.run(debug=False)