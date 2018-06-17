import os
import tempfile
import pytest
import config
from app import app, db


@pytest.fixture
def client():
    app.config.from_object(config.Config)
    app.config.from_envvar('WOLFIT_SETTINGS')
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()
    db.session.close()
    db.drop_all()
    db.create_all()

    yield client
