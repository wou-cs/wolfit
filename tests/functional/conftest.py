import os
import tempfile
import pytest
from app import app, db


# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     client = app.test_client()
#     db.session.close()
#     db.drop_all()
#     db.create_all()

#     yield client
