import pytest
from blog import create_app
from blog.models import db, User, Post
from blog import config


@pytest.fixture(scope='module')
def new_user():
    user = User('phuoctv14', 'phuoctv14@gmail.com', '123456')
    return user


@pytest.fixture(scope='module')
def test_client(user):
    flask_app = create_app(config_class=config.TestingConfig)

    # Flask provides a way to test your application by exposing the Werkzeug
    # test client and handling the context locals
    test_client = flask_app.test_client()

    # Establish an application context before running the test
    ctx = flask_app.app_context()
    ctx.push()

    yield test_client  # this is where testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    # create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(username='phuoctv14', email='phuoctv14@gmail.com',
                 password='123456')
    user2 = User(username='test1', email='test1@email.com',
                 password='password')
    db.session.add(user1)
    db.session.add(user2)

    # commit the changes for the users
    db.session.commit()

    yield db  # this is where testing happens!
    db.drop_all()



