import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import config


app = Flask(__name__)
app.config.from_object(config.Config)
app.config.from_envvar('WOLFIT_SETTINGS')

SECRET_KEY = app.config['SECRET_KEY']
if not SECRET_KEY:
    raise ValueError("No secret key set for Flask application")

app.config['SQLALCHEMY_DATABASE_URI'] = config.Config.DATABASE_URI(app)

db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)

from app import routes, models
