from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
import secrets
from blog.forms import RegistrationForm, LoginForm, SearchForm

app = Flask(__name__)


app.config['SECRET_KEY'] = str(secrets.token_hex(16))

# app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# db=SQLAlchemy(app)

posts = []


@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html', title='Index', form=form)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == 'password':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Log in', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    return render_template('search.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

