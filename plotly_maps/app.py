from flask import Flask
from flask import Flask, jsonify, json, render_template, Markup
from bs4 import BeautifulSoup
import requests

    

# SQL Alchemy
from sqlalchemy import create_engine, func, extract

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

# #################################################
# # Database Setup
# #################################################


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
@app.route("/plotly")
def home():
    return render_template("index.html")


@app.route("/gender_growth_over_years")
def gender_count():
    # year_list = []
    # year = session.query(func.extract('year', Loans.posted_time).distinct())
    # for years in year:
    #     year_list.append(years)
    # print(year_list)
    sel = [func.sum(Loans.female_count).label('female_borrower_count'), func.sum(Loans.male_count).label('male_borrower_count'), func.extract("year", Loans.posted_time), Loans.country_name]
    results = session.query(*sel).\
        group_by(Loans.country_name,(func.extract("year", Loans.posted_time))).all()

    # print(results)   
    

    master_list = {}

    for result in results:
        gender_yeardata = {}
        
        gender_yeardata['YEAR'] = result[2]
        gender_yeardata['FEMALE'] = int(result[0])
        gender_yeardata['MALE'] = int(result[1])
        #gender_count_year.append(gender_yeardata)

        if  result[3]  in master_list:
            master_list
            # print ("result[3]" + result[3])
            master_list[result[3]].append(gender_yeardata)
        else :
            
            master_list[result[3]] = [gender_yeardata]
            # print ( master_list )


    return jsonify(master_list)


@app.route("/genderwise_popular_sector")
def sector_popularity():
    
    sel = [func.sum(Loans.female_count).label('female_borrower_count'), func.sum(Loans.male_count).label('male_borrower_count'), Loans.sector_name,Loans.country_name]
    results = session.query(*sel).\
        group_by(Loans.country_name,Loans.sector_name).all()

    # print(results)

    master_list_sector = {}

    for result in results:
        sector_data = {}
        sector_data['Female'] = int(result[0])
        sector_data['Male'] = int(result[1])
        sector_data['Sector'] = (result[2])

        if  result[3] in master_list_sector:
            master_list_sector
            # print ("result[3]" + result[3])
            master_list_sector[result[3]].append(sector_data)
        else :
            
            master_list_sector[result[3]] = [sector_data]
        

    return jsonify(master_list_sector)

@app.route("/topCountries")
def topCountries():
    sel = [func.count(Loans.loan_id), Loans.country_name]
    results = session.query(*sel).\
        group_by(Loans.country_name).order_by(func.count(Loans.loan_id).desc()).all()

    # print(results)
    top_3_Countries = []
    for result in results:
        country_details = {}
        country_details["Country"] = (result[1])
        country_details["NumberOfLoans"] = int(result[0])
        top_3_Countries.append(country_details)

    return jsonify(top_3_Countries)

@app.route("/topCountriesByLoanCount")
def topCountry():
    return render_template("topCountry.html")



@app.route("/philippinesData")
def philippinesData():
    sel = session.query(Loans.sector_name, Loans.activity_name, Loans.loan_amount_usd, Loans.country_name, func.count(Loans.loan_id), Loans.num_lenders_total).filter(Loans.country_name == "Philippines").\
    group_by(Loans.sector_name).all()
   
    return jsonify(sel)



@app.route("/kenyaData")
def kenyaData():
    sel = session.query(Loans.sector_name, Loans.activity_name, Loans.loan_amount_usd, Loans.country_name, func.count(Loans.loan_id), Loans.num_lenders_total).filter(Loans.country_name == "Kenya").\
    group_by(Loans.sector_name).all()
   
    return jsonify(sel)



@app.route("/peruData")
def peruData():
    sel = session.query(Loans.sector_name, Loans.activity_name, Loans.loan_amount_usd, Loans.country_name, func.count(Loans.loan_id), Loans.num_lenders_total).filter(Loans.country_name == "Peru").\
    group_by(Loans.sector_name).all()
   
    return jsonify(sel)


if __name__ == "__main__":
    app.run(debug=True)