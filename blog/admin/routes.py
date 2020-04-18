from flask_admin.contrib.sqla import ModelView
from blog.models import User, Post
from blog import db, admin


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
