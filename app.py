# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 10:21:37 2022

@author: NWANDU KELECHUKWU
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from WikiLovesMonument_Database import user_contribution_count


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Project.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Contribution(db.Model):

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String, unique=True)
        dataresponse = db.Column(db.Text, unique=True)
        

        def __init__(self, name, dataresponse):
                self.name = name
                self.dataresponse = dataresponse
                                                                                 

if __name__ == '__main__':
        #db.create_all()
        freq_count = user_contribution_count('Category:Images_from_Wiki_Loves_Monuments_2017_in_Brazil')
        year2017contribution = Contribution("Year2017", freq_count)
        db.session.add(year2017contribution)
        db.session.commit() 
        print('done')    

