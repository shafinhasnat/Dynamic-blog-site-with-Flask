from flask import Flask, escape, request, render_template,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shafinsblog'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['DATABASE_URL'] = 'sqlite:///site.db'
db=SQLAlchemy(app)
############pore add kora hoise
db.create_all()
##############
bcrypt= Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = 'Access denied! Please login first.'
login_manager.login_message_category = 'danger'

from flaskblog import routes