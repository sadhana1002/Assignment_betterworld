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

from datetime import datetime, date
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
# Utility functions
#################################################

def get_countries():
    countries = session.query(Country.country, Country.longitude, Country.latitude).all()
    
    country_dict = {}
    
    for c in countries:
        c_dict = {
            c[0]:[c[1],c[2]]
        }
        
        country_dict.update(c_dict)
        
    
    return country_dict

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

@app.route("/loans_timeline")
def all_loans():
    results = session.query(sqlalchemy.func.year(Loans.posted_time ),
                            sqlalchemy.func.month(Loans.posted_time ),
                            sqlalchemy.func.sum(Loans.loan_amount_usd),
                            Loans.sector_name,
                            Country.country).join(Country, Loans.country_code==Country.country_code).group_by(
                            sqlalchemy.func.year(Loans.posted_time ),
                            sqlalchemy.func.month(Loans.posted_time ),
                            Loans.sector_name,
                            
                            Country.country).all()
    
    loans_timeseries = []
    
    country_geo = get_countries()
    
    for row in results:
        loan = {
            'month_year':date(row[0],row[1],1),
            'loan_amount': row[2],
            'sector':row[3],
            'country_name':row[4],
            'geo': country_geo[row[4]]
        }
        
        loans_timeseries.append(loan)
        
    return jsonify(loans_timeseries)

if __name__ == "__main__":
    app.run(debug=True)