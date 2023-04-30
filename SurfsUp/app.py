# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
import datetime as dt
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def main():
    return (
        f"Welcome to the Climate Home Page<br>"
        f"Where you can go:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"
    )

# -----------------------------------------------------------
    
@app.route("/api/v1.0/precipitation")
def prcp():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    precip_dict = dict(precip)
    session.close()
    return jsonify(precip_dict)

# ------------------------------------------------------------

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Measurement.station, func.count(Measurement.id)).\
        group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()
    stations_dict = dict(stations)
    session.close()
    return jsonify(stations_dict)

# --------------------------------------------------------------

@app.route("/api/v1.0/tobs")
def tobs():
    max_tobs = session.query(Measurement.station, Measurement.tobs)\
    .filter(Measurement.date >= '2016-08-23')\
    .all()
    tobs_dict = dict(max_tobs)
    session.close()
    return jsonify(tobs_dict)

# ----------------------------------------------------------------

@app.route("/api/v1.0/<start>")
def start():
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                                func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    session.close()
    tobs_all = []

    for min,avg,max in result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_all.append(tobs_dict)
        
    return jsonify(tobs_all)

# -----------------------------------------------------------------

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs).\
                func.max(Measurement.tobs)).filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()

    session.close()
    tobs_all = []
    
    for min,avg,max in result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_all.append(tobs_dict)

    return jsonify(tobs_all)

# ----------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)