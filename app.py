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

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\NWANDU KELECHUKWU\Desktop\outreachy\code\Model\WLM.db' 

edition = db.Table('Edition', db.metadata, autoload=True, autoload_with=db.engine)
photograph = db.Table('Photograph', db.metadata, autoload=True, autoload_with=db.engine)
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
def dashboard():
    puser = db.session.query(photograph).filter_by(edition_year="2022", person_id=1).count()
    puser2015 = db.session.query(photograph).filter_by(edition_year="2015",person_id=1).count()
    puser2016 = db.session.query(photograph).filter_by(edition_year="2016",person_id=1).count()
    puser2018 = db.session.query(photograph).filter_by(edition_year="2018",person_id=1).count()
    puser2019 = db.session.query(photograph).filter_by(edition_year="2019",person_id=1).count()
    puser2020 = db.session.query(photograph).filter_by(edition_year="2020",person_id=1).count()
    puser2021 = db.session.query(photograph).filter_by(edition_year="2021",person_id=1).count()
    puser2022 = db.session.query(photograph).filter_by(edition_year="2022",person_id=1).count()
    
    #print(puser2015, puser2016, puser2018, puser2019, puser2020, puser2021, puser2022)
    return render_template('index.html', user_cont=puser, puser2015=puser2015, puser2016=puser2016, puser2018=puser2018, puser2019=puser2019, puser2020=puser2020, puser2021=puser2021, puser2022=puser2022)

@app.route('/stats')
def ranking():
    edition2022 = db.session.query(edition).filter_by(year=2022).all()
    photograph2022 = db.session.query(photograph).filter_by(edition_year="2022").count()
    photograph2021 = db.session.query(photograph).filter_by(edition_year="2021").count()
    
    #print(edition2022[0])
    #print(photograph2022)
    return render_template('stats.html', edition2=edition2022[0], photograph1=photograph2021, photograph2=photograph2022)
 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)