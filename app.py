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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/methane.db"
db = SQLAlchemy(app)
#

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

class Beef(db.Model):
    __tablename__ = "meat_data"
    Country = Column(String, primary_key=True)
    CountryCode = Column(String)
    Continent = Column(String)
    Region = Column(String, nullable=True)
    Year = Column(Integer, nullable=True)
    Population = Column(Integer, nullable=True)
    TotalBeefConsumption = Column(Integer, nullable=True)
    BeefConsumptionPerCapita = Column(Integer)

    def __repr__(self):
        return '<Beef %r>' % (self.country)

#engine = create_engine("sqlite:///db/methane.db")
#conn = engine.connect()

##Base.metadata.create_all(engine)

##from sqlalchemy.orm import Session
#session = Session(bind=engine)

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/emissions_data")
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

    results = db.session.query(*sel).all()

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


@app.route("/meat_consumption")
def index2():
    """Return the homepage."""
    return render_template("index2v2.html")

@app.route("/meat_data")
def getBeef():
    """Return the MetaData for a given sample."""
    sel = [
        Beef.Country,
        Beef.CountryCode,
        Beef.Continent,
        Beef.Region,
        Beef.Year,
        Beef.Population,
        Beef.TotalBeefConsumption,
	    Beef.BeefConsumptionPerCapita
        ]

    results = db.session.query(*sel).all()

   # Create a dictionary entry for each row of metadata information
    beef_list = []

    for result in results: 
        beef_metadata = {}
        beef_metadata["Country"] = result[0]
        beef_metadata["CountryCode"] = result[1]
        beef_metadata["Continent"] = result[2]
        beef_metadata["Region"] = result[3]
        beef_metadata["Year"] = result[4]
        beef_metadata["Population"] = result[5]
        beef_metadata["TotalBeefConsumption"] = result[6]
        beef_metadata["BeefConsumptionPerCapita"] = result[7]
        beef_list.append(beef_metadata)

        print(beef_list)
    return jsonify(beef_list)




if __name__ == "__main__":
    app.run(debug=True, port=8000)