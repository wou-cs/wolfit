from app.models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email, and password fields are defined correctly
    """
    new_user = User(
        username='robot',
        email='robot@gmail.com')
    assert new_user.username == 'robot'
    assert new_user.email == 'robot@gmail.com'
    new_user.set_password('FlaskIsAwesome')
    assert new_user.password_hash != 'FlaskIsAwesome'
    assert new_user.check_password('FlaskIsAwesome')
    assert not new_user.check_password('Another password')
