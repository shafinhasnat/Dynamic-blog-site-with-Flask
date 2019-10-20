from flask import Flask, escape, request, render_template,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shafinsblog'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

######################################################
# app.config.from_object(os.environ['APP_SETTINGS'])	 #
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #
######################################################




ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:19971904@localhost/koyafalan'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://expsyuworaprov:7757f6a756cf696088337a2abe67de9d7672133dbf5c3d5363f99c598c532ba0@ec2-174-129-194-188.compute-1.amazonaws.com:5432/dacgacsoi62src'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False






db=SQLAlchemy(app)

bcrypt= Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = 'Access denied! Please login first.'
login_manager.login_message_category = 'danger'

from flaskblog import routes