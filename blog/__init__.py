# init
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import secrets
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = str(secrets.token_hex(16))
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

crypt = Bcrypt(app)

# use flask-login extension to manage login
login_manger = LoginManager(app)
login_manger.login_view = 'login'
login_manger.login_message_category = 'info'

# config mail sever for this app
app.config['MAIL_USE_SMTP'] = True
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
# you need to export to environment: export EMAIL_USER=... and for EMAIL_PASS too
# your email need to turn on less secure app on google (if you use google)
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

# import routes in here
from blog import routes




