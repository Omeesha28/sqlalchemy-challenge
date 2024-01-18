# Import the dependencies.
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
Base.prepare(autoload_with=engine)

# Save references to each table
Measurment = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def Homepage():
    """List all available api routes."""
    return (
        f"Welcome to the SQLAlchemy App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the precipitation data"""
    # Query all precipitation
    results = session.query(Measurment.date, Measurment.prcp).filter(Measurment.date >= "2016-08-23").filter(Measurment.date <= "2017-08-23").all()

    session.close()

    all_the_precipitations = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["prcp"] = prcp
        all_the_precipitations.append(prcp_dict)

    return jsonify(all_the_precipitations)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the stations data"""
    # Query all precipitation
    results = session.query(Measurment.station, func.count(Measurment.station)).group_by(Measurment.station).order_by(func.count(Measurment.station).desc()).all()

    #Convert the results from list to dictionaries
    station_data = list(np.ravel(results))

    session.close()

    #Return results in Jsonify 
    return jsonify(station_data)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the stations data"""
    # Query all Tobs
    most_active_station_number = 'USC00519281'
    results = session.query(Measurment.date, Measurment.tobs).\
                        filter(Measurment.date >= "2016-08-24").\
                        filter(Measurment.date <= "2017-08-23").\
                        filter(Measurment.station == most_active_station_number).all()

    #Convert the results from list to dictionaries
    all_the_tobs = []
    for prcp, date,tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_the_tobs.append(tobs_dict)
    
    session.close()

    #Return results in Jsonify 
    return jsonify(all_the_tobs)

@app.route("/api/v1.0/<start>")
def start_date(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the stations data"""
    # Query all Tobs
    results = session.query(Measurment.date).order_by(Measurment.date.desc()).first()

    #Convert the results from list to dictionaries
    start_date = []
    for min, avg, max in results:
        start_date_dict = {}
        start_date_dict["min_temp"] = min
        start_date_dict["avg_temp"] = avg
        start_date_dict["max_temp"] = max
        start_date.append(start_date_dict)     
    
    session.close()

    #Return results in Jsonify 
    return jsonify(start_date)

@app.route("/api/v1.0/<start>/<end>")
def start_and_end_date(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the stations data"""
    # Query all Tobs
    results = session.query(func.min(Measurment.tobs), func.avg(Measurment.tobs), func.max(Measurment.tobs)).filter(Measurment.date >= start_date).filter(Measurment.date <= end_date).all()
    
    #Convert the results from list to dictionaries
    start_and_end_date = []
    for min, avg, max in results:
        start_and_end_date_dict = {}
        start_and_end_date_dict["min_temp"] = min
        start_and_end_date_dict["avg_temp"] = avg
        start_and_end_date_dict["max_temp"] = max
        start_and_end_date.append( start_and_end_date_dict)  
    
    session.close()

    #Return results in Jsonify 
    return jsonify( start_and_end_date)

if __name__ == '__main__':
    app.run(debug=True)
