#!/usr/bin/env python

""" 
    Parses the config.json file from the home folder into a global variable and connects to the db
    Populate the database with tables by running db.py
"""

import os
import json
import logging

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)

config_data = open(os.path.expanduser("~/config.json"),"r").read()
config = json.loads(config_data)

Base = declarative_base()

engine = create_engine(config["db_connection"])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
 
class Phonebook(Base):
    __tablename__ = 'phonebook'
    
    id = Column(Integer, primary_key=True)
    addr = Column(String(250), nullable=False)
    city = Column(String(250), nullable=False)
    state = Column(String(250), nullable=False)
    zip_code = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    phone = Column(String(250), nullable=False)
    used = Column(Boolean, nullable=False)

class Zipcodes(Base):
    __tablename__ = 'zipcodes'
    
    id = Column(Integer, primary_key=True)
    zip_code = Column(String(250), nullable=False)
    city = Column(String(250), nullable=False)
    state = Column(String(250), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

if __name__ == "__main__":

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)