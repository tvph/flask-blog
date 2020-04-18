"""
This file (test_models.py) contains the unit tests for the models.py file
"""


def test_empty_db(client):
    """
    START with a blank database
    """

    rv = client.get('/')
    assert b'No entries here so far' in rv.data


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_valid_login_logout(client, init_database):
    """
    Given a Flask app
    When the '/login' page is posted to (POST)
    Then check the response is valid
    """
    response = client.post('/login', data=dict(email='phuoctv14@gmail.com',
                                               password='12345'), follow_redirects=True)
    assert response.status_code == 200

    """
    Given the Flask app
    When the '/logout' page is requested (POST)
    Then check the response is valid
    """
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    