from flask import Blueprint, render_template, request
from blog.models import Post
from flask_login import login_required
from blog.users.forms import LoginForm

main = Blueprint('main', __name__)


@main.route('/')
def index():
    form = LoginForm()
    return render_template('login.html', title='Index', form=form)


@main.route('/home')
@login_required
def home():
    # set page from request, default to 1, type: int
    page = request.args.get('page', 1, type=int)
    # use sqlalchemy pagination
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, title='Home')
