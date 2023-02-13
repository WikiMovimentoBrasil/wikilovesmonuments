# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 10:21:37 2022

@author: NWANDU KELECHUKWU
"""
from flask import Flask
from flask import render_template

# Flask constructor takes the name of
# current module (__name__) as argument.

from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\NWANDU KELECHUKWU\Desktop\outreachy\code\Model\WLM.db' 

edition = db.Table('Edition', db.metadata, autoload=True, autoload_with=db.engine)
photograph = db.Table('Photograph', db.metadata, autoload=True, autoload_with=db.engine)
monument_photograph = db.Table('Monument_photograph', db.metadata, autoload=True, autoload_with=db.engine)
monument = db.Table('Monument', db.metadata, autoload=True, autoload_with=db.engine)
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
def dashboard():
    presentyear = date.today().year
    #monumentid = "photograph id"
    puser = db.session.query(photograph).filter_by(edition_year=str(presentyear-1), person_id=1).count()
    puser2015 = db.session.query(photograph).filter_by(edition_year=str(presentyear-8),person_id=1).count()
    puser2016 = db.session.query(photograph).filter_by(edition_year=str(presentyear-7),person_id=1).count()
    puser2018 = db.session.query(photograph).filter_by(edition_year=str(presentyear-5),person_id=1).count()
    puser2019 = db.session.query(photograph).filter_by(edition_year=str(presentyear-4),person_id=1).count()
    puser2020 = db.session.query(photograph).filter_by(edition_year=str(presentyear-3),person_id=1).count()
    puser2021 = db.session.query(photograph).filter_by(edition_year=str(presentyear-2),person_id=1).count()
    puser2022 = db.session.query(photograph).filter_by(edition_year=str(presentyear-1),person_id=1).count()
    
    data = db.session.query(photograph).filter_by(person_id=1).subquery()
    dataa = db.session.query(monument_photograph).join(data, data.c.monument_id == monument_photograph.c["photograph id"]).subquery()
    mapcoords = db.session.query(monument.c.geographic_coordinates).join(dataa, monument.c.wikidata_qid == dataa.c["photograph id"]).all()
    mapdetails = db.session.query(monument.c.image_filename).join(dataa, monument.c.wikidata_qid == dataa.c["photograph id"]).all()
    
    return render_template('index.html', details=mapdetails, coordinate=mapcoords, user_cont=puser, puser2015=puser2015, puser2016=puser2016, puser2018=puser2018, puser2019=puser2019, puser2020=puser2020, puser2021=puser2021, puser2022=puser2022)

@app.route('/stats')
def ranking():
    presentyear = date.today().year
    edition2022 = db.session.query(edition).filter_by(year=presentyear-1).all()
    photograph2015 = db.session.query(photograph).filter_by(edition_year=str(presentyear-8)).count()
    photograph2016 = db.session.query(photograph).filter_by(edition_year=str(presentyear-7)).count()
    photograph2018 = db.session.query(photograph).filter_by(edition_year=str(presentyear-5)).count()
    photograph2019 = db.session.query(photograph).filter_by(edition_year=str(presentyear-4)).count()
    photograph2020 = db.session.query(photograph).filter_by(edition_year=str(presentyear-3)).count()
    photograph2021 = db.session.query(photograph).filter_by(edition_year=str(presentyear-2)).count()
    photograph2022 = db.session.query(photograph).filter_by(edition_year=str(presentyear-1)).count()
    #ch = db.session.query(photograph).filter_by(edition_year="2015", person_id=14).all()
    e1 = db.session.query(edition).filter_by(year=2022).subquery()
    #ch2 = db.session.query(photograph).join(edition, edition.c.place_2 == photograph.c.filename).all()
    
    #data = db.session.query(photograph).filter_by(person_id=1).subquery()
    dataa = db.session.query(photograph.c.photograph).join(e1, e1.c.place_1 == photograph.c.filename).all()
    #mapdata = db.session.query(monument.c.geographic_coordinates).join(dataa, monument.c.wikidata_qid == dataa.c["photograph id"]).all()
    print(dataa)
    return render_template('stats.html', edition2022=edition2022[0], photograph2015=photograph2015, photograph2016=photograph2016, photograph2018=photograph2018, photograph2019=photograph2019, photograph2020=photograph2020, photograph2021=photograph2021, photograph2022=photograph2022)


@app.route('/stats/<year>')
def stats_year(year):
    editionyear = db.session.query(edition).filter_by(year=int(year)).all()
    photographyear = db.session.query(photograph).filter_by(edition_year=year).count()
    photographeryear = db.session.query(photograph).filter_by(edition_year=year).group_by(photograph.c.photograph).count()
    
    print(photographeryear)
    # show the user profile for that user
    return render_template('statsyear.html', year=year, editionyear=editionyear[0], photographyear=photographyear, photographeryear=photographeryear)

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)