from flask import request, render_template, flash, redirect, url_for, abort
from blog.forms import RegistrationForm, LoginForm, SearchForm, UpdateForm, PostForm
from blog.models import User, Post
from blog import app, db, crypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image


# app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/')
def index():
    form = LoginForm()
    return render_template('login.html', title='Index', form=form)


@app.route('/home')
@login_required
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts, title='Home')


# save profile pictures into /static/pictures folder
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)  # make random hex string
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_name)
    # resize picture before save it
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    # save it
    img.save(picture_path)
    return picture_name


@app.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.picture = picture_file
        
        current_user.email = form.email.data
        # hash new password and then save it
        new_pwd_hashed = crypt.generate_password_hash(form.new_password.data)
        current_user.password = new_pwd_hashed
        db.session.commit()
        flash(f'Your account have been update', 'success')
        return redirect(url_for('about'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    # render to about page
    picture = url_for('static', filename='pictures/' + current_user.picture)
    return render_template('about.html', title='About', picture=picture, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    # check validation when submit form in register page
    if form.validate_on_submit():
        hashed_pwd = crypt.generate_password_hash(
            form.password.data).decode('utf-8')  # generate hashed password
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account have been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create.html', title='New post', form=form)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(404)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f'Your post have been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create.html', title='Update post', form=form)


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(404)
    
    db.session.delete(post)
    db.session.commit()
    flash(f'Your post have been deleted.', 'success')
    return redirect(url_for('home'))
    
    