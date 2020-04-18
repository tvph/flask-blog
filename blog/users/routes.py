from flask import (Blueprint, flash, redirect,
                   url_for, render_template, request)
from flask_login import login_required, login_user, current_user, logout_user
from blog import crypt, db
from blog.models import User, Post
from blog.users.forms import (UpdateForm, RegistrationForm,
                              LoginForm, RequestResetForm, ResetPasswordFrom)
from blog.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)


@users.route('/about', methods=['GET', 'POST'])
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
        return redirect(url_for('users.about'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    # render to about page
    picture = url_for('static', filename='pictures/' + current_user.picture)
    return render_template('about.html', title='About',
                           picture=picture, form=form)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    # check validation when submit form in register page
    if form.validate_on_submit():
        hashed_pwd = crypt.generate_password_hash(
            form.password.data).decode('utf-8')  # generate hashed password
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account have been created! You are now able to log in',
              'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and crypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Log in', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/user/<string:username>', methods=['GET'])
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    # query all users with user name
    user = User.query.filter_by(username=username).first_or_404()
    # query all posts of that user above
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f'An email sent with instructions to reset your password.',
              'info')
        redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset password',
                           form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if not user:
        flash(f'That is invalid token', 'warning')
        return redirect(url_for('users.reset_password'))
    form = ResetPasswordFrom()
    if form.validate_on_submit():
        hashed_password = crypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated. You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
