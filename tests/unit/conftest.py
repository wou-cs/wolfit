import os
import tempfile
import pytest
from app import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Because we will often be testing forms where tracking CSRF will be a pain,
    # let's turn off validation during testing.
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()
    db.session.close()
    db.drop_all()
    db.create_all()

    yield client
