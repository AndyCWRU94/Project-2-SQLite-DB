import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float


from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#Create an app
app = Flask(__name__)
#Base = declarative_base()
# The database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///methane.db"
db = SQLAlchemy(app)

class Emissions(db.Model):
    __tablename__ = "emissions_data"
    Country = Column(String, primary_key=True)
    Country_Code = Column(String)
    Continent = Column(String)
    Region = Column(String, nullable=True)
    Year = Column(Integer, nullable=True)
    Population = Column(Integer, nullable=True)
    Emissions = Column(Integer, nullable=True)
    Emissions_Per_Capita = Column(Integer)

    def __repr__(self):
        return '<Emissions %r>' % (self.country)

engine = create_engine("sqlite:///methane.db")
conn = engine.connect()

Base.metadata.create_all(engine)

from sqlalchemy.orm import Session
session = Session(bind=engine)

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/emissions_data/")
def getEmissions():
    """Return the MetaData for a given sample."""
    sel = [
        Emissions.Country,
        Emissions.Country_Code,
        Emissions.Continent,
        Emissions.Region,
        Emissions.Year,
        Emissions.Population,
        Emissions.Emissions,
	    Emissions.Emissions_Per_Capita
        ]

    results = session.query(*sel).all()

   # Create a dictionary entry for each row of metadata information
    emissions_list = []

    for result in results: 
        emissions_metadata = {}
        emissions_metadata["Country"] = result[0]
        emissions_metadata["Country_Code"] = result[1]
        emissions_metadata["Continent"] = result[2]
        emissions_metadata["Region"] = result[3]
        emissions_metadata["Year"] = result[4]
        emissions_metadata["Population"] = result[5]
        emissions_metadata["Emissions"] = result[6]
        emissions_metadata["Emissions_Per_Capita"] = result[7]
        emissions_list.append(emissions_metadata)

        print(emissions_list)
        return jsonify(emissions_list)


if __name__ == "__main__":
    app.run(port=8000)