from flask import request, render_template, flash, redirect, url_for
from blog.forms import RegistrationForm, LoginForm, SearchForm
from blog.models import User, Post
from blog import app, db, crypt
from flask_login import login_user, current_user, logout_user, login_required

# app.config.from_object(os.environ['APP_SETTINGS'])
posts = []


@app.route('/')
@app.route('/home')
def home():
    form = LoginForm()
    return render_template('home.html', title='Home')


@app.route('/about')
@login_required
def about():
    picture = url_for('static', filename='pictures/' + current_user.picture)
    return render_template('about.html', title='About', picture=picture)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = crypt.generate_password_hash(form.password.data).decode('utf-8')  # generate hashed password
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account have been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and crypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Log in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    return render_template('search.html')
