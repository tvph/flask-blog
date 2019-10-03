from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
# from models import User
# from datetime import datetime
import datetime


app = Flask(__name__)


app.config['SECRET_KEY'] = '1a94670cb42475d42189'

# app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# db=SQLAlchemy(app)

posts = [
    {
        'author': 'tran viet phuoc',
        'title': 'blog post 1',
        'content': 'first blog content',
        'date_posted': datetime.date(2019, 8, 20)
    },
    {
        'author': 'phuoc tran viet',
        'title': 'blog post 2',
        'content': 'second blog content',
        'date_posted': datetime.date(2019, 8, 21)
    }
]


@app.route('/')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')

# @app.route('register',method=['GET','POST'])
# def register():


#  @app.route('login',method=['GET','POST'])
#  def login():


if __name__ == '__main__':
    app.run(debug=True)