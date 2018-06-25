import pytest
from flask import url_for
from app import app, db
from app.models import User, Post


def login(client, username, password):
    return client.post(
        url_for("login"),
        data=dict(username=username, password=password),
        follow_redirects=True,
    )


def logout(client):
    return client.get(url_for("logout"), follow_redirects=True)


def test_no_posts_no_user(client):
    """Start with a blank database."""

    response = client.get(url_for("index"))
    assert b"No entries" in response.data
    assert b"Anonymous" in response.data


def test_no_posts_logged_in_user(client, test_user):
    """
    Given a new system with just a registered user
    When the user logs in
    Then they should be greeted in person but see no posts
    """
    response = login(client, test_user.username, "yoko")
    assert response.status_code == 200
    assert b"No entries" in response.data
    assert b"john" in response.data


def test_should_be_anon_after_logout(client, test_user):
    """
    Given a new system with just a registered user
    When the user logs in then logs out
    Then the site should greet them as anonymous
    """
    response = login(client, test_user.username, "yoko")
    assert response.status_code == 200
    assert b"john" in response.data
    response = logout(client)
    assert b"Anonymous" in response.data


def test_should_see_single_post(client, single_post):
    """
    Given there is a single post created
    When an anonymous user visits the site
    Then the user should see the post headline
    """
    response = client.get(url_for("index"))
    assert b"First post" in response.data
    assert b"Anonymous" in response.data


def test_should_see_login_form_when_not_logged_in(client, single_post):
    response = client.get(url_for("login"))
    assert b"Sign In" in response.data
    assert b"Username" in response.data


def test_user_should_be_redirected_to_index_if_logged_in(client, test_user):
    login(client, test_user.username, "yoko")
    response = client.get(url_for("login"))
    assert response.status_code == 302
    assert "/index" in response.headers["Location"]


def test_bad_password_should_be_redirected_to_login(client, test_user):
    response = client.post(
        url_for("login"),
        data=dict(username=test_user.username, password="paul"),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_empty_post_should_be_redirected_to_login(client, test_user):
    response = client.post(url_for("login"), follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_there_should_be_a_place_for_new_users_to_register(client):
    response = client.post(url_for("register"))
    assert response.status_code == 200
    assert b"Register" in response.data


def test_should_be_a_link_to_register_if_not_logged_in(client):
    response = client.get(url_for("login"))
    assert b"Register" in response.data


def test_register_should_create_a_new_user(client):
    response = client.post(
        url_for("register"),
        data=dict(
            username="john", email="john@beatles.com", password="yoko", password2="yoko"
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200
    u = db.session.query(User).filter_by(username="john").one()
    assert u.email == "john@beatles.com"


def test_user_should_have_a_profile_page(client, test_user):
    login(client, test_user.username, "yoko")
    response = client.get(url_for("user", username=test_user.username))
    assert response.status_code == 200
    assert test_user.username.encode() in response.data


def test_user_should_have_nav_link_to_profile(client, test_user):
    response = login(client, test_user.username, "yoko")
    assert b"Profile" in response.data


def test_profile_should_show_posts_for_that_user(
    client, test_user, single_post, random_post
):
    login(client, test_user.username, "yoko")
    response = client.get(url_for("user", username=test_user.username))
    assert single_post.title.encode() in response.data
    assert random_post.title.encode() not in response.data
    assert url_for("post", id=single_post.id, _external=False).encode() in response.data


def test_index_with_posts_should_have_links_to_details(client, single_post):
    response = client.get(url_for("index"))
    assert url_for("post", id=single_post.id, _external=False).encode() in response.data


def test_post_should_have_detail_page_with_body(client, single_post):
    response = client.get(url_for("post", id=single_post.id))
    assert single_post.body.encode() in response.data
