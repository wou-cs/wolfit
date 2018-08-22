import pytest
import textwrap
from datetime import timedelta
from app.models import User, Post
from app import db
from sqlalchemy import exc


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email, and password fields are defined correctly
    """
    new_user = User(username="robot", email="robot@gmail.com")
    assert new_user.username == "robot"
    assert new_user.email == "robot@gmail.com"
    new_user.set_password("FlaskIsAwesome")
    assert new_user.password_hash != "FlaskIsAwesome"
    assert new_user.check_password("FlaskIsAwesome")
    assert not new_user.check_password("Another password")


def test_user_as_string():
    username = "robot"
    new_user = User(username=username, email="robot@gmail.com")
    assert username in str(new_user)


def test_post_as_string():
    title = "First post"
    new_post = Post(title=title)
    assert title in str(new_post)


def test_post_body_markdown_render():
    body = textwrap.dedent(
        """\
        Start of the body

        * Bullet 1
        * [Bullet 2](http://example.com)
    """
    )
    new_post = Post(title="Foo", body=body)
    assert "<ul>" in new_post.body_as_html()
    assert "<a href=" in new_post.body_as_html()


def test_recent_posts_should_be_ordered(client, test_user, single_post):
    single_post.timestamp = single_post.timestamp - timedelta(days=1)
    db.session.add(single_post)
    db.session.commit()
    p = Post(title="Recent post", body="More current", user_id=test_user.id)
    db.session.add(p)
    db.session.commit()
    assert p.title == Post.recent_posts()[0].title
    assert single_post.title == Post.recent_posts()[-1].title


def test_posts_should_have_a_vote_count():
    p = Post(title="New post", body="Not interesting", vote_count=0)
    assert p.vote_count == 0


def test_post_should_have_proper_status_for_user_when_new(
    client, test_user, single_post
):
    assert not single_post.already_voted(test_user)


def test_post_vote_count_goes_up_after_voting(client, test_user, single_post):
    assert single_post.vote_count == 0
    single_post.up_vote(test_user)
    assert single_post.vote_count == 1


def test_a_user_can_only_vote_once(client, test_user, single_post):
    single_post.up_vote(test_user)
    single_post.up_vote(test_user)  # Should throw an exception
    assert single_post.vote_count == 1
