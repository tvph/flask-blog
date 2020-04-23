# init
from flask import Flask
# flask sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# to hash password
from flask_bcrypt import Bcrypt
# to manage login/session
from flask_login import LoginManager
# to send mail from server
from flask_mail import Mail

from blog.config import Config
# migrating database
from flask_migrate import Migrate
# admin panel
from flask_admin import Admin


# initialize Flask admin panel
admin = Admin(name='Blog', template_mode='boostrap4')

# use flask_sqlalchemy extension
db = SQLAlchemy()

# use flask_bcrypt extension
crypt = Bcrypt()

# use flask-login extension to manage login
login_manger = LoginManager()
login_manger.login_view = 'users.login'  # use blueprint
login_manger.login_message_category = 'info'

# use flask_mail exentsion
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # init all extensions with app
    db.init_app(app)
    crypt.init_app(app)
    login_manger.init_app(app)
    mail.init_app(app)
    # Admin panel
    admin.init_app(app)

    # init migrating database
    # use flask cli to run: flask db init or pipenv run python manage.py db init
    # to create migrations folder
    migrate = Migrate()
    migrate.init_app(app, db)

    # import all blueprints here
    from blog.users.routes import users
    from blog.posts.routes import posts
    from blog.main.routes import main
    from blog.errors.handlers import errors
    # import admin blueprint
    from blog.admin import admin_bp

    # then run these blueprints
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    # add admin blueprint
    app.register_blueprint(admin_bp)
    
    return app
