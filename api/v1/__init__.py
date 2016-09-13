from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, init_db
from os import remove

api = "/api/v1"

########################################
####       !!!  WARNING  !!!        ####
####   For dev environment only     ####
####   This reinit the whole DB     ####
########################################
# db_path = "db/osldev.db"
# remove(db_path)
########################################

app = Flask(__name__)
app.config.from_pyfile("../../setup.py")

sqlite_path = app.config["SQLALCHEMY_DATABASE_URI"]

init_db(sqlite_path)


engine = create_engine(sqlite_path)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
DBSession.bind = engine
session = DBSession()

from company import *
from user import *
from team import *
