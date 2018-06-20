import pytest
import time
from flask import url_for
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from app import app, db
from app.models import User, Post

PASSWORD = "yoko"
MAX_WAIT = 10


class TestLoggedInUser(object):
    @pytest.fixture(autouse=True)
    def execute(self, client):
        client.begin()
        yield
        client.end()

    def wait_for_element(self, client, id, text):
        start_time = time.time()
        while True:
            try:
                element = client.browser.find_element_by_id(id).text
                assert text in element
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.25)

    def test_login(self, client, test_user):
        client.browser.get(client.get_server_url())
        login_link = client.browser.find_element_by_id("nav-login-link")
        login_link.click()
        self.wait_for_element(client, "page-title", "Login")
        login_name = client.browser.find_element_by_id("username")
        login_name.send_keys(test_user.username)
        password = client.browser.find_element_by_id("password")
        password.send_keys('yoko')
        password.send_keys(Keys.ENTER)
        self.wait_for_element(client, "user-greeting", test_user.username)
