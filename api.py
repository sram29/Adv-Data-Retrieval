# Python SQL toolkit and Object Relational Mapper
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from datetime import datetime

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii2.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Assign the stations class to a variable called `Station`
Station = Base.classes.station

# Assign the measurements class to a variable called `Measure`
Measure = Base.classes.measurement

# Create a session
session = Session(engine)

# create flask api
app = Flask(__name__)

# Home
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/temp<br>"
        f"/api/v1.0/after/'enter start date in %Y-%m-%d format'<br>"
        f"/api/v1.0/between/'enter start date in %Y-%m-%d format'/'enter end date in %Y-%m-%d format'<br>"
    )

# precipitaion
@app.route("/api/v1.0/precipitation")
def prcp():
    """Query for the dates and precipitation observations from the last year"""
    
    start_date = '2017-01-01'

    prcp_data = (session
                 .query(Measure.date, Measure.prcp)
                 .filter(Measure.date >= start_date)
                 .all())
    
    prcp_list = []
    
    for result in prcp_data:
        
        row = {}
        
        row[str(result[0])] = result[1]
        
        prcp_list.append(row)
        
    return jsonify(prcp_list)

# stations
@app.route("/api/v1.0/stations")
def station_listss():
    """Query for the stations"""
    station_lists = (session
                .query(Station)
                .all())

    stations_list = []
    
    for station in station_lists:
    
        row = {}
        row['station'] = station.station
        row['name'] = station.name
        row['latitude'] = station.latitude
        row['longitude'] = station.longitude
        row['elevation'] = station.elevation

        stations_list.append(row)
        
    return jsonify(stations_list)       

# Temperature
@app.route("/api/v1.0/temp")
def temp():
    """Query for the dates and temperature observations from the last year"""
    
    start_date = '2017-01-01'

    temp_data = (session
                 .query(Measure.date, Measure.temp)
                 .filter(Measure.date >= start_date)
                 .all())
    
    temp_list = []
    
    for result in temp_data:
        
        row = {}
        
        row[str(result[0])] = result[1]
        
        temp_list.append(row)
        
    return jsonify(temp_list)

# start end
@app.route("/api/v1.0/after")
@app.route("/api/v1.0/after/<start>")
def temp_analysis_after(start='2017-01-01'):
    
    # query for min temp
    temp_min = (session
                .query(func.min(Measure.temp))
                .filter(Measure.date >= start)
                .scalar())
    
    # query for max temp
    temp_max = (session
                .query(func.max(Measure.temp))
                .filter(Measure.date >= start)
                .scalar())  
    
    # query for average temp
    temp_avg = (session
                .query(func.avg(Measure.temp))
                .filter(Measure.date >= start)
                .scalar())
    
    temp_dict= {}
    
    temp_dict['min'] = temp_min
    
    temp_dict['max'] = temp_max
    
    temp_dict['average'] = temp_avg
    
    return jsonify(temp_dict)


@app.route("/api/v1.0/between")
@app.route("/api/v1.0/between/<start>/<end>")
def temp_analysis_between(start='2017-01-01', end='2017-12-31'):
    
    # query for min temp
    temp_min = (session
                .query(func.min(Measure.temp))
                .filter(Measure.date >= start)
                .filter(Measure.date <= end)
                .scalar())
    
    # query for max temp
    temp_max = (session
                .query(func.max(Measure.temp))
                .filter(Measure.date >= start)
                .filter(Measure.date <= end)
                .scalar())  
    
    # query for average temp
    temp_avg = (session
                .query(func.avg(Measure.temp))
                .filter(Measure.date >= start)
                .filter(Measure.date <= end)
                .scalar())
    
    temp_dict= {}
    
    temp_dict['min'] = temp_min
    
    temp_dict['max'] = temp_max
    
    temp_dict['average'] = temp_avg
    
    return jsonify(temp_dict)

if __name__ == '__main__':
    app.run(debug=True)