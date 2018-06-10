import os
import tempfile
import pytest
from app import app


@pytest.fixture
def client():
    # db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    print(f"DB: {app.config['SQLALCHEMY_DATABASE_URI']}")
    app.config['TESTING'] = True
    client = app.test_client()

    # with app.app_context():
    #     app.init_db()

    yield client

    # os.close(db_fd)
    # os.unlink(app.config['DATABASE'])
