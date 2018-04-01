from flask import Flask
from flask import Flask, jsonify, render_template
    

# SQL Alchemy
from sqlalchemy import create_engine

# PyMySQL 
import pymysql
pymysql.install_as_MySQLdb()

# Create Engine and Pass in MySQL Connection
engine = create_engine("mysql://root:Mkashi029@@localhost:3306/kiva")
conn = engine.connect()

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# #################################################
# # Database Setup
# #################################################
# engine = create_engine('mysql://scott:tiger@localhost/kiva')

# # reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# # Save references to each table
print (Base.classes)
Loans = Base.classes.loans
Country = Base.classes.country

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/gender_disperity")
def gender_count():
    results = session.query(
    func.sum(Loans.female_count).label('female_count'), func.sum(Loans.male_count).label('male_count'), Loans.country_name,
    Country.latitude,Country.longitude
    ).join(Country, Loans.country_code==Country.country_code
    ).group_by(Loans.country_name
    ).all()
    #print(results)

    gender_count_country = []

    # Create a dictionary entry for each row of metadata information
    
    for result in results:
        gender_metadata = {}
        gender_metadata['COUNTRY'] = result[2]
        gender_metadata['FEMALE'] = int(result[0])
        gender_metadata['MALE'] = int(result[1])
        gender_metadata['LATITUDE'] = int(result[3])
        gender_metadata['LONGITUDE'] = int(result[4])
        gender_count_country.append(gender_metadata)
        
    return jsonify(gender_count_country)


if __name__ == "__main__":
    app.run(debug=True)