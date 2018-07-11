import textwrap
from datetime import timedelta
from app.models import User, Post
from app import db


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
    body = textwrap.dedent("""\
        Start of the body

        * Bullet 1
        * [Bullet 2](http://example.com)
    """)
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
