# import necessary libraries
# import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect

# PyMySQL 
import pymysql

# Create Engine and Pass in MySQL Connection
engine = create_engine(f"mysql://{user}:{password}@localhost:3306/kiva")

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

# Create empty list to get column names for querying

column_list_loans = []
column_list_country = []
for column in loans.__table__.columns:
    column_list_loans.append(column.key)
for column in country.__table__.columns:
    column_list_country.append(column.key)

print(column_list_country)
print(column_list_loans)


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


if __name__ == "__main__":
    app.run()

