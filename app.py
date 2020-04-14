import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes['measurement']
station = Base.classes['station']

last_date = '2017-08-23'
one_year = '2016-08-22'

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date > '2016-08-22').\
    order_by(measurement.date).all()

    session.close()

    all_prcp = []
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict["date"] = date
        measurement_dict["precipitation"] = prcp
        all_prcp.append(measurement_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date > one_year, measurement.station == 'USC00519281').\
    all()

    session.close()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(results))

    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def tobs_start_date(start):

    session = Session(engine)

    results = session.query(func.max(measurement.tobs),\
    func.avg(measurement.tobs),func.min(measurement.tobs)).\
    filter(measurement.date > start, measurement.station == 'USC00519281').\
    all()

    session.close()

    # Convert list of tuples into normal list
    start_results = list(np.ravel(results))

    return (f"Since the date {start}, the maxiumum daily temperature,\
        the average daily temperature, and the minimum daily temperature were: </br> {start_results}")
        

@app.route("/api/v1.0/<start>/<end>")
def tobs_start_end_date(start, end):

    session = Session(engine)

    results = session.query(func.max(measurement.tobs),\
    func.avg(measurement.tobs),func.min(measurement.tobs)).\
    filter(measurement.date > start, measurement.date < end,\
    measurement.station == 'USC00519281').all()

    session.close()

    # Convert list of tuples into normal list
    start_close_results = list(np.ravel(results))

    return (f"Between the dates of {start} and {end}, the maxiumum daily temperature,\
        the average daily temperature, and the minimum daily temperature were: </br> {start_close_results}")

if __name__ == '__main__':
    app.run(debug=True)
