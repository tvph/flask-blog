from flask import (render_template, redirect, url_for, flash, request,
    abort, Blueprint)
from flask_login import current_user, login_required
from blog import db
from blog.models import Post
from blog.posts.forms import PostForm, SearchForm


posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create.html', title='New post', form=form)


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create.html', title='Update post', form=form)


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your post have been deleted.', 'success')
    return redirect(url_for('main.home'))


@posts.route('/search', methods=['GET'])
@login_required
def search():
    # get keyword by form request
    keyword = request.args.get('keyword')
    if request.method == 'GET':
        # search in Post.content by matching with keyword, then get paginate of it
        posts = Post.query.filter(Post.content.like('%' + keyword + '%')).order_by(Post.id).paginate(per_page=20)
        if posts is None:
            return redirect(url_for('errors.error_404', 404))
        flash(f'Here is your result', 'success')
        return render_template('home.html', title='Search', posts=posts)