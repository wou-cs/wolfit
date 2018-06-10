import pytest
from flask import url_for
from app import db
from app.models import User


@pytest.fixture
def test_user():
    u = User(username='john', email='john@beatles.com')
    u.set_password('yoko')
    db.session.add(u)
    db.session.commit()
    return u


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


# def logout(client):
#     return client.get('/logout', follow_redirects=True)


def test_no_posts_no_user(client):
    """Start with a blank database."""

    result = client.get('/')
    assert b'No entries' in result.data
    assert b'Anonymous' in result.data


def test_no_posts_loggin_in_user(client, test_user):
    """
    Given a new system with just a registered user
    When the user logs in
    Then they should be greeted in person but see no posts
    """
    users = User.query.all()
    print(f"NUMBER OF USERS: { len(users) }")
    response = client.post('/login', data=dict(
        username=test_user.username,
        password='yoko'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'No entries' in response.data
    assert b'john' in response.data
