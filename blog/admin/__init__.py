'''Admin blueprint'''
from flask import Blueprint


admin_bp = Blueprint('admin_bp', __name__)
# then import routes from blog.admin blueprint
from blog.admin import routes