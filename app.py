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
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\NWANDU KELECHUKWU\Desktop\outreachy\code\Model\wikilovesmonuments.db' 

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
    puser = db.session.query(photograph).filter_by(edition_year=str(presentyear-1), person_id=261).count()
    puser2015 = db.session.query(photograph).filter_by(edition_year=str(presentyear-8),person_id=261).count()
    puser2016 = db.session.query(photograph).filter_by(edition_year=str(presentyear-7),person_id=261).count()
    puser2018 = db.session.query(photograph).filter_by(edition_year=str(presentyear-5),person_id=261).count()
    puser2019 = db.session.query(photograph).filter_by(edition_year=str(presentyear-4),person_id=261).count()
    puser2020 = db.session.query(photograph).filter_by(edition_year=str(presentyear-3),person_id=261).count()
    puser2021 = db.session.query(photograph).filter_by(edition_year=str(presentyear-2),person_id=261).count()
    puser2022 = db.session.query(photograph).filter_by(edition_year=str(presentyear-1),person_id=261).count()
    
    data1 = db.session.query(photograph).filter_by(person_id=261).all()
    data = db.session.query(photograph).filter_by(person_id=261).subquery()
    #dataa = db.session.query(monument_photograph).join(data, data.c.monument_id == monument_photograph.c["photograph id"]).subquery()
    #monumentcoords = db.session.query(monument.c.geographic_coordinates).outerjoin(dataa, monument.c.wikidata_qid == dataa.c["photograph id"]).all()
    #monumentdetails = db.session.query(monument.c.image_filename).join(dataa, monument.c.wikidata_qid == dataa.c["photograph id"]).all()
    #photographcoords = db.session.query(photograph.c.camera_coordinates).filter_by(person_id=261).all()
    #photographdetails = db.session.query(photograph.c.filename).filter_by(person_id=261).all()
    monumentcoords = db.session.query(monument.c.geographic_coordinates).filter(data.c.id == monument.c.id).all()
    photographcoords = db.session.query(data.c.camera_coordinates).filter(data.c.id == monument.c.id).all()
    monumentdetails = db.session.query(monument.c.image_filename).filter(data.c.id == monument.c.id).all()
    photographdetails = db.session.query(data.c.filename).filter(data.c.id == monument.c.id).all()
    
    #print(monumentcoords)
    #print(photographcoords)
    #print(photographdetails)
    #print(monumentdetails)
    return render_template('index.html', photographdetails=photographdetails, monumentdetails=monumentdetails,  photographcoordinate=photographcoords, monumentcoordinate=monumentcoords, user_cont=puser, puser2015=puser2015, puser2016=puser2016, puser2018=puser2018, puser2019=puser2019, puser2020=puser2020, puser2021=puser2021, puser2022=puser2022)

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
    
    editionyear = db.session.query(edition).filter_by(year=str(presentyear-1)).subquery()
    winner_1 = db.session.query(photograph).join(editionyear, editionyear.c.place_1 == photograph.c.filename).all()
    winner_2 = db.session.query(photograph).join(editionyear, editionyear.c.place_2 == photograph.c.filename).all()
    winner_3 = db.session.query(photograph).join(editionyear, editionyear.c.place_3 == photograph.c.filename).all()
    winner_4 = db.session.query(photograph).join(editionyear, editionyear.c.place_4 == photograph.c.filename).all()
    winner_5 = db.session.query(photograph).join(editionyear, editionyear.c.place_5 == photograph.c.filename).all()
    winner_6 = db.session.query(photograph).join(editionyear, editionyear.c.place_6 == photograph.c.filename).all()
    winner_7 = db.session.query(photograph).join(editionyear, editionyear.c.place_7 == photograph.c.filename).all()
    winner_8 = db.session.query(photograph).join(editionyear, editionyear.c.place_8 == photograph.c.filename).all()
    winner_9 = db.session.query(photograph).join(editionyear, editionyear.c.place_9 == photograph.c.filename).all()
    winner_10 = db.session.query(photograph).join(editionyear, editionyear.c.place_10 == photograph.c.filename).all()
    #print(winner_1)
    return render_template('stats.html', edition2022=edition2022[0], photograph2015=photograph2015, photograph2016=photograph2016, photograph2018=photograph2018, photograph2019=photograph2019, photograph2020=photograph2020, photograph2021=photograph2021, photograph2022=photograph2022)#, winner_1=winner_1[0], winner_2=winner_2[0], winner_3=winner_3[0], winner_4=winner_4[0], winner_5=winner_5[0], winner_6=winner_6[0], winner_7=winner_7[0], winner_8=winner_8[0], winner_9=winner_9[0], winner_10=winner_10[0])


@app.route('/stats/<year>')
def stats_year(year):
    editionyear = db.session.query(edition).filter_by(year=int(year)).all()
    photographyear = db.session.query(photograph).filter_by(edition_year=year).count()
    photographeryear = db.session.query(photograph).filter_by(edition_year=year).group_by(photograph.c.photographer).count()
    editionyearsub = db.session.query(edition).filter_by(year=year).subquery()
    winner_1 = db.session.query(photograph).join(editionyearsub, editionyearsub.c.place_1 == photograph.c.filename).all()
    winner_2 = db.session.query(photograph).join(editionyearsub, editionyearsub.c.place_2 == photograph.c.filename).all()
    winner_3 = db.session.query(photograph).join(editionyearsub, editionyearsub.c.place_3 == photograph.c.filename).all()
    winner_4 = db.session.query(photograph).join(editionyearsub, editionyearsub.c.place_4 == photograph.c.filename).all()
    winner_5 = db.session.query(photograph).join(editionyearsub, editionyearsub.c.place_5 == photograph.c.filename).all()
    winner_6 = db.session.query(photograph).join(editionyearsub, editionyearsub.c.place_6 == photograph.c.filename).all()
    winner_7 = db.session.query(photograph).join(editionyearsub, editionyearsub.c.place_7 == photograph.c.filename).all()
    winner_8 = db.session.query(photograph).join(editionyearsub, editionyearsub.c.place_8 == photograph.c.filename).all()
    winner_9 = db.session.query(photograph).join(editionyearsub, editionyearsub.c.place_9 == photograph.c.filename).all()
    winner_10 = db.session.query(photograph).join(editionyearsub, editionyearsub.c.place_10 == photograph.c.filename).all()
    print(winner_1)
    # show the user profile for that user
    return render_template('statsyear.html', year=year, editionyear=editionyear[0], photographyear=photographyear, photographeryear=photographeryear, winner_1=winner_1[0])#, winner_2=winner_2[0], winner_3=winner_3[0], winner_4=winner_4[0], winner_5=winner_5[0], winner_6=winner_6[0], winner_7=winner_7[0], winner_8=winner_8[0], winner_9=winner_9[0], winner_10=winner_10[0])

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def page_not_found(e):
    return render_template("404.html")

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)