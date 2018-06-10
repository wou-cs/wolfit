from app.models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email, and hashed_password fields are defined correctly
    """
    new_user = User('robot', 'robot@gmail.com', 'FlaskIsAwesome')
    assert new_user.username == 'robot'
    assert new_user.email == 'robot@gmail.com'
    assert new_user.hashed_password != 'FlaskIsAwesome'
