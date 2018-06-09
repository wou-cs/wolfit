from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('default_settings')
app.config.from_envvar('WOLFIT_DEV_SETTINGS')

db = SQLAlchemy(app)
