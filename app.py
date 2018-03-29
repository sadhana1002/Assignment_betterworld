# import necessary libraries
# import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect


from flask import (
    Flask,
    render_template,
    jsonify)

#################################################
# Database Setup
#################################################
# engine = create_engine("database_goes_here")

# reflect an existing database into a new model
# Base = automap_base()
# reflect the tables
# Base.prepare(engine, reflect=True)

# Create our session (link) from Python to the DB
# session = Session(engine)



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

