import os
import tempfile
import pytest
import config
import threading
import time
import multiprocessing
from app import app, db
from selenium import webdriver


class LiveClient(object):
    def __init__(self):
        app.config.from_object(config.Config)
        app.config.from_envvar("WOLFIT_SETTINGS")
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["LIVESERVER_PORT"] = 5000
        # app.config['SERVER_NAME'] = 'localhost'

    def get_server_url(self):
        """
        Return the url of the test server
        """
        return "http://localhost:5000"

    def begin(self):
        db.session.close()
        db.drop_all()
        db.create_all()
        self.ctx = app.app_context()
        self.browser = webdriver.Chrome()

        # Start Flask server in a thread
        threading.Thread(target=app.run).start()

        # give the server a second to ensure it is up
        time.sleep(1)
        self.ctx.push()

    def end(self):
        # remove application context
        self.ctx.pop()
        self.browser.get(f"{(self.get_server_url())}/shutdown")
        self.browser.quit()


@pytest.fixture(scope="module")
def client():
    return LiveClient()
