import pytest
from flask import url_for
from app import app, db
from app.models import User, Post

import time


class TestAnonymousUser(object):
    @pytest.fixture(autouse=True)
    def execute(self, client):
        client.begin()
        yield
        client.end()

    def test_no_posts_no_user(self, client):
        client.browser.get(client.get_server_url())
        assert "Wolfit" in client.browser.title
        greeting = client.browser.find_element_by_id("user-greeting").text
        assert "Anonymous" in greeting

    def test_navigation_when_not_logged_in(self, client):
        client.browser.get(client.get_server_url())
        nav = client.browser.find_element_by_id("nav-home").find_element_by_xpath(
            ".//a"
        )
        assert "index" in nav.get_attribute("href")
        nav = client.browser.find_element_by_id("nav-login").find_element_by_xpath(
            ".//a"
        )
        assert "login" in nav.get_attribute("href")
