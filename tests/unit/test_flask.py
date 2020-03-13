"""
This file (test_models.py) contains the unit tests for the models.py file
"""


def test_empty_db(client):
    """
    START with a blank database
    """

    rv = client.get('/')
    assert b'No entries here so far' in rv.data

