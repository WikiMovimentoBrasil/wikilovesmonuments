# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 10:21:37 2022

@author: NWANDU KELECHUKWU
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from WikiLovesMonument_Database import user_contribution_count


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Project.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class person(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String)
        data_created = db.Column(db.Text)
        

        def __init__(self, username, data_created):
                self.username = username
                self.data_created = data_created
                                                                                 

class photograph(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        filename = db.Column(db.String)
        photograph = db.Column(db.String)
        monument_id = db.Column(db.String)
        license = db.Column(db.String)
        timestamp_uploaded = db.Column(db.Text)
        timestamp_created = db.Column(db.Text)
        camera_model = db.Column(db.String)
        geographic_coordinates = db.Column(db.String)
        edition = db.Column(db.String)
        

        def __init__(self, filename, photograph, monument_id, license, timestamp_uploaded, timestamp_created, camera_model, geographic_coordinates, edition):
                self.filename = filename
                self.photograph = photograph
                self.monument_id = monument_id
                self.license = license
                self.timestamp_uploaded = timestamp_uploaded
                self.timestamp_created =  timestamp_created
                self.camera_model =  camera_model
                self.geographic_coordinates = geographic_coordinates
                self.edition =  edition
                                                                                 

class monument(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        wikidata_qid = db.Column(db.String)
        country = db.Column(db.String)
        located_at = db.Column(db.String)
        geographic_coordinates = db.Column(db.Text)
        address = db.Column(db.String)
        common_category = db.Column(db.String)
        image_filename = db.Column(db.String)
        last_modified = db.Column(db.Text)
        

        def __init__(self, wikidata_qid, country, located_at, geographic_coordinates, address, common_category, image_filename, last_modified):
                self.wikidata_qid = wikidata_qid
                self.country = country
                self.located_at = located_at
                self.geographic_coordinates = geographic_coordinates
                self.address = address
                self.common_category = common_category
                self.image_filename = image_filename
                self.last_modified = last_modified
                                                                                   

class edition(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        year = db.Column(db.Integer)
        country = db.Column(db.String)
        place_1 = db.Column(db.String)
        place_2 = db.Column(db.String)
        place_3 = db.Column(db.String)
        place_4 = db.Column(db.String)
        place_5 = db.Column(db.String)
        place_6 = db.Column(db.String)
        place_7 = db.Column(db.String)
        place_8 = db.Column(db.String)
        place_9 = db.Column(db.String)
        place_10 = db.Column(db.String)
        

        def __init__(self, year, country, place_1, place_2, place_3, place_4, place_5, place_6, place_7, place_8, place_9, place_10):
                self.year = year
                self.country = country
                self.place_1 = place_1
                self.place_2 = place_2
                self.place_3 = place_3
                self.place_4 = place_4
                self.place_5 = place_5
                self.place_6 = place_6
                self.place_7 = place_7
                self.place_8 = place_8
                self.place_9 = place_9
                self.place_10 = place_10



if __name__ == '__main__':
        db.create_all()
        #freq_count = user_contribution_count('Category:Images_from_Wiki_Loves_Monuments_2018_in_Brazil')
        #year2018contribution = Contribution("Year2018", freq_count)
        #db.session.add(year2018contribution)
        db.session.commit() 
        print('done')    

