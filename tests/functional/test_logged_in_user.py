import pytest
import time
from flask import url_for
from selenium.webdriver.common.keys import Keys
from app import app, db
from app.models import User, Post
from test_live_server import TestLiveServer

PASSWORD = "yoko"


class TestLoggedInUser(TestLiveServer):

    def test_login(self, client, test_user):
        client.browser.get(client.get_server_url())
        self.wait_for_element(client, "nav-login", "Login")
        login_link = client.browser.find_element_by_id("nav-login-link")
        login_link.click()
        self.wait_for_element(client, "page-title", "Login")
        login_name = client.browser.find_element_by_id("username")
        login_name.send_keys(test_user.username)
        password = client.browser.find_element_by_id("password")
        password.send_keys('yoko')
        password.send_keys(Keys.ENTER)
        self.wait_for_element(client, "user-greeting", test_user.username)
