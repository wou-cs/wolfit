from app.models import User, Post


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
    body = ("Start of the body\n"
            "\n"
            "* Bullet 1\n"
            "* [Bullet 2](http://example.com)\n"
            "\n")
    new_post = Post(title="Foo", body=body)
    assert "<ul>" in new_post.body_as_html()
    assert "<a href=" in new_post.body_as_html()
