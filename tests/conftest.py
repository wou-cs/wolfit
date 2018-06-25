import pytest
from app import db
from app.models import User, Post

USERNAME = 'john'
PASSWORD = 'yoko'


@pytest.fixture
def test_user():
    u = User(username=USERNAME, email='john@beatles.com')
    u.set_password(PASSWORD)
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def single_post():
    user = db.session.query(User).filter_by(username=USERNAME).first()
    if user is None:
        user = test_user()
    p = Post(title='First post', body='Something saucy', user_id=user.id)
    db.session.add(p)
    db.session.commit()
    return p
