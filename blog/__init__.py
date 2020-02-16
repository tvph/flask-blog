from blog.app import app
from blog.models import db

with app.test_request_context():
    db.init_app(app)
    db.create_all()