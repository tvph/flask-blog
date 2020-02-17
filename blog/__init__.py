# init
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets


app = Flask(__name__)

app.config['SECRET_KEY'] = str(secrets.token_hex(16))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/site.db'

db = SQLAlchemy(app)

from blog import routes




