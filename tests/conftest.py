import pytest
from blog import create_app
from blog.models import User, Post, db
from blog import config
import tempfile


@pytest.fixture(scope='module')
def new_user():
    user = User('phuoctv14', 'phuoctv14@gmail.com', '123456')
    return user


@pytest.fixture(scope='module')
def client():
    flask_app = create_app(config_class=config.TestingConfig)

    # Flask provides a way to test your application by exposing the Werkzeug
    # test client and handling the context locals test_client() method
    # Establish an application context before running the test use 
    # context manager
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client

    # ctx = flask_app.app_context()
    # ctx.push()

    # yield test_client  # this is where testing happens!

    # ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    # create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User()
    user1.username = 'phuoctv14'
    user1.email = 'phuoctv14@gmail.com'
    user1.password = '123456'
    db.session.add(user1)

    # commit the changes for the users
    db.session.commit()

    yield db  # this is where testing happens!
    db.drop_all()




