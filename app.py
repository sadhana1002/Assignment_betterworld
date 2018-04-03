# import necessary libraries
# import pandas as pd
from credentials import user, password
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# PyMySQL 
import pymysql
pymysql.install_as_MySQLdb()
# Create Engine and Pass in MySQL Connection
engine = create_engine("mysql://root:booboohead1337@localhost:3306/kiva")

#################################################
# Database Setup
#################################################


# Create Base
Base = automap_base()
Base.prepare(engine, reflect = True)

# Create our session (link) from Python to the DB
session = Session(engine)
conn = engine.connect()

# Set tables

loans = Base.classes.loans
country = Base.classes.country
flags = Base.classes.flags

# Create empty list to get column names for querying

column_list_loans = []
column_list_country = []
for column in loans.__table__.columns:
    column_list_loans.append(column.key)
for column in country.__table__.columns:
    column_list_country.append(column.key)

# print(column_list_country)
# print(column_list_loans)


from flask import (
    Flask,
    render_template,
    jsonify)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

# route queries and returns a list of the country names. will be used to populate dropdown
@app.route("/countries")
def get_countries():
    results = session.query(loans.country_name)
    countries = []
    for a in results:
        countries.append(a.country_name)
    countries = set(countries)
    clean = []
    for a in countries:
        clean.append(a)
    
    return jsonify(clean)

# Get country info
@app.route("/countries/<country>")
def get_country_info(country):
    country = country.capitalize()
    results = session.query(loans).\
        filter(loans.country_name == country).all()
    full_dict = []
    for result in results:
        current_dict = {}
        current_dict["name"] = result.country_name
        current_dict["country_code"] = result.country_code
        current_dict["loan_id"] = result.loan_id
        current_dict["status"] = result.status
        current_dict["sector"] = result.sector_name
        current_dict["activity"] = result.activity_name
        current_dict["posted"] = result.posted_time
        current_dict["disbursed"] = result.disburse_time
        current_dict["raised"] = result.raised_time
        current_dict["term"] = result.lender_term
        current_dict["total_lenders"] = result.num_lenders_total
        current_dict["interval"] = result.repayment_interval
        current_dict["female"] = result.female_count
        current_dict["male"] = result.male_count
        current_dict["borrowers"] = result.borrower_count
        current_dict["funded_amount"] = result.funded_amount_usd
        current_dict["loan_amount"] = result.loan_amount_usd
        current_dict["shortage_amount"] = result.shortage_fund
        full_dict.append(current_dict)
    
    return jsonify(full_dict)

# Route to get flag url
@app.route("/flag/<country>")
def get_country_flag(country):
    country = country.capitalize()
    flag_query = session.query(flags).\
        filter(flags.country == country)
    for flag in flag_query:
        flag_dict = {}
        flag_dict["country"] = flag.country
        flag_dict["url"] = flag.url

    return jsonify(flag_dict)


if __name__ == "__main__":
    app.run(debug=True)

