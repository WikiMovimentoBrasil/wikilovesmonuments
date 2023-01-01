# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 10:21:37 2022

@author: NWANDU KELECHUKWU
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from WikiLovesMonument import user_contribution_count


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Project.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class ronti(db.Model):

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String, unique=True)
        year2015 = db.Column(db.Text, unique=True)
        

        def __init__(self, name, year2015):
                self.name = name
                self.year2015 = year2015
                                                                                 

if __name__ == '__main__':
        #db.create_all()
        me = ronti("mart", '{"crew": 3}')
        db.session.add(me)
        db.session.commit() 
        print('done')    
 