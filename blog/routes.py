from flask import request, render_template, flash, redirect, url_for
from blog.forms import RegistrationForm, LoginForm, SearchForm
from blog.models import User, Post
from blog import app


# app.config.from_object(os.environ['APP_SETTINGS'])
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
