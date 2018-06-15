import pytest
from flask import url_for
from app import db
from app.models import User, Post


@pytest.fixture
def test_user():
    u = User(username='john', email='john@beatles.com')
    u.set_password('yoko')
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def single_post():
    user = test_user()
    p = Post(title='First post', body='Something saucy', user_id=user.id)
    db.session.add(p)
    db.session.commit()
    return p


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_no_posts_no_user(client):
    """Start with a blank database."""

    response = client.get('/')
    assert b'No entries' in response.data
    assert b'Anonymous' in response.data


def test_no_posts_logged_in_user(client, test_user):
    """
    Given a new system with just a registered user
    When the user logs in
    Then they should be greeted in person but see no posts
    """
    response = login(client, test_user.username, 'yoko')
    assert response.status_code == 200
    assert b'No entries' in response.data
    assert b'john' in response.data


def test_should_be_anon_after_logout(client, test_user):
    """
    Given a new system with just a registered user
    When the user logs in then logs out
    Then the site should greet them as anonymous
    """
    response = login(client, test_user.username, 'yoko')
    assert response.status_code == 200
    assert b'john' in response.data
    response = logout(client)
    assert b'Anonymous' in response.data


def test_should_see_single_post(client, single_post):
    """
    Given there is a single post created
    When an anonymous user visits the site
    Then the user should see the post headline
    """
    response = client.get('/')
    assert b'First post' in response.data
    assert b'Anonymous' in response.data


def test_should_see_login_form_when_not_logged_in(client, single_post):
    response = client.get('/login')
    assert b'Sign In' in response.data
    assert b'Username' in response.data


def test_user_should_be_redirected_to_index_if_logged_in(client, test_user):
    login(client, test_user.username, 'yoko')
    response = client.get('/login')
    assert response.status_code == 302
    assert "/index" in response.headers["Location"]


def test_bad_password_should_be_redirected_to_login(client, test_user):
    response = client.post('/login', data=dict(
        username=test_user.username,
        password="paul",
    ), follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_empty_post_should_be_redirected_to_login(client, test_user):
    response = client.post('/login', follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]
