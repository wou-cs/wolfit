import os
import tempfile
from sqlalchemy.orm import scoped_session, sessionmaker

import config

import pytest

from app import app, db


@pytest.fixture
def test_app():
    app.config.from_object(config.Config)
    app.config.from_envvar("WOLFIT_SETTINGS")
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SERVER_NAME"] = "test.local"

    yield app


@pytest.fixture
def test_db(test_app):
    # Pushing the app context allows us to make calls to the app like url_for
    # as if we were the running Flask app. Makes testing routes more resiliant.
    with test_app.app_context():
        db.create_all()

        yield test_db

        db.drop_all()


@pytest.fixture
def client(test_app, test_db):
    with test_app.app_context():
        with test_app.test_client() as client:
            yield client


