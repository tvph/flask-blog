# init
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import secrets


app = Flask(__name__)

app.config['SECRET_KEY'] = str(secrets.token_hex(16))
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

crypt = Bcrypt(app)
login_manger = LoginManager(app)  # use flask-login extension to manage login
login_manger.login_view = 'login'
login_manger.login_message_category = 'info'

# import routes in here
from blog import routes




