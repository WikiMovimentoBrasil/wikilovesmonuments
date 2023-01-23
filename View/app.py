# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 10:21:37 2022

@author: NWANDU KELECHUKWU
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from WLMfunctions import get_all_files_cat, get_username, get_culturalheritage, get_location, get_coordinate, get_street, get_monumentid, get_winners, get_categories, get_last_modified, get_last_created, get_camera_name, get_license, get_registration

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\NWANDU KELECHUKWU\Desktop\outreachy\code\Model\WLM.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Person(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String, unique=True)
        date_created = db.Column(db.Text)
        photographs = db.relationship("Photograph", backref="Person")
        

        def __init__(self, username, date_created):
                self.username = username
                self.date_created = date_created



class Edition(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        year = db.Column(db.Integer, unique=True)
        country = db.Column(db.String, unique=True)
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
        photograph1 = db.relationship("Photograph", backref="Edition")
        
        

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



monument_photograph = db.Table("monument_photograph",
        db.Column("monument id", db.Integer, db.ForeignKey("monument.id")),
        db.Column("photograph id", db.Integer, db.ForeignKey("photograph.monument_id"))
)


class Photograph(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        filename = db.Column(db.String, unique=True)
        photograph = db.Column(db.String)
        monument_id = db.Column(db.String)
        license = db.Column(db.String)
        timestamp_uploaded = db.Column(db.Text)
        timestamp_created = db.Column(db.Text)
        camera_model = db.Column(db.String)
        geographic_coordinates = db.Column(db.String)
        edition_year = db.Column(db.String)
        person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
        edition_id = db.Column(db.Integer, db.ForeignKey("edition.id"))
        detail = db.relationship("Monument", secondary=monument_photograph, backref="photo_details")
        

        def __init__(self, filename, photograph, monument_id, license, timestamp_uploaded, timestamp_created, camera_model, geographic_coordinates, edition_year, person_id, edition_id):
                self.filename = filename
                self.photograph = photograph
                self.monument_id = monument_id
                self.license = license
                self.timestamp_uploaded = timestamp_uploaded
                self.timestamp_created =  timestamp_created
                self.camera_model =  camera_model
                self.geographic_coordinates = geographic_coordinates
                self.edition_year =  edition_year
                self.person_id = person_id
                self.edition_id = edition_id                                          

class Monument(db.Model):
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

def get_or_create(session, model, **args):
    '''
    Creates an object or returns the object if exists
    credit to Kevin @ StackOverflow
    from: http://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
    '''

    instance = session.query(model).filter_by(**args).first()
    if instance:
        return instance
    else:
        instance = model(**args)
        db.session.add(instance)
        return instance                                                                                   


if __name__ == '__main__':

        db.create_all()
        
        for file in get_all_files_cat('Category:Images_from_Wiki_Loves_Monuments_2015_in_Brazil'):
    
                antique = get_or_create(db.session, Monument, wikidata_qid=get_culturalheritage(file), country="Brazil", located_at=get_location(file), geographic_coordinates=get_coordinate(file), address=get_street(file), common_category=get_categories(file), image_filename=file, last_modified=get_last_modified(file))
                user = get_or_create(db.session, Person, username=get_username(file), date_created=get_registration(file))
                antique_edition = get_or_create(db.session, Edition, year="2015", country="Brazil", place_1=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[0], place_2=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[1], place_3=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[2], place_4=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[3], place_5=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[4], place_6=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[5], place_7=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[6], place_8=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[7], place_9=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[8], place_10=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[9])
                antique_photo = get_or_create(db.session, Photograph, filename=file, photograph=get_username(file), monument_id=get_culturalheritage(file), license=get_license(file), timestamp_uploaded=get_last_modified(file), timestamp_created=get_last_created(file), camera_model=get_camera_name(file), geographic_coordinates=get_coordinate(file), edition_year="2015", person_id=user.id, edition_id=antique_edition.id)
                        
                db.session.add_all([antique, antique_photo])
                
                antique_photo.detail.append(antique) #adding many-to-many relationship data
                user.photographs.append(antique_photo)
                
                db.session.commit() 
                print('done')  
        

        '''
        for user in get_unique_username('Category:Images_from_Wiki_Loves_Monuments_2015_in_Brazil'):
                lois = Person(
                antique_edition = Edition(year="2015", country="Brazil", place_1=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[0], place_2=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[1], place_3=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[2], place_4=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[3], place_5=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[4], place_6=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[5], place_7=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[6], place_8=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[7], place_9=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[8], place_10=get_winners('Wiki_Loves_Monuments_2015_winners#Brazil')[9])
                        
                #antique_edition.photograph1.append(antique_photo) #adding one-to-many relationship data i.e edition to photograph
                #lois.photographs.append(antique_photo) #adding one-to-many relationship data i.e person to photograph
                
                db.session.add_all([lois, antique_edition])
                db.session.commit() 
                print('finally') '''