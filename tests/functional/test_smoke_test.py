import os
import tempfile
from flask import Flask, url_for
from flask_testing import LiveServerTestCase
import pytest
from app import app, db
from app.models import User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PASSWORD = 'yoko'


class IntegrationTest(LiveServerTestCase):
    def create_app(self):
        self.client = app.test_client()
        db.session.close()
        db.drop_all()
        db.create_all()
        return app

    def setUp(self):
        self.app = self.create_app()
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_get_page(self):
        self.browser.get(self.get_server_url())
        assert "Wolfit" in self.browser.title
        greeting = self.browser.find_element_by_id("user-greeting").text
        assert 'Anonymous' in greeting

    def test_navigation_when_not_logged_in(self):
        self.browser.get(self.get_server_url())
        nav = self.browser.find_element_by_id('nav-home').find_element_by_xpath(".//a")
        assert url_for('index') in nav.get_attribute('href')
        nav = self.browser.find_element_by_id('nav-login').find_element_by_xpath(".//a")
        assert url_for('login') in nav.get_attribute('href')


# class AuthenticatedTest(LiveServerTestCase):
#     @pytest.fixture(autouse=True)
#     def authenticated_user(self):
#         u = User(username='john', email='john@beatles.com')
#         u.set_password(PASSWORD)
#         db.session.add(u)
#         db.session.commit()
#         self.browser.get(url_for('login'))
#         # self.wait_for_element("page-title", "Login")
#         login_name = self.browser.find_element_by_id("username")
#         login_name.send_keys(u.username)
#         password = self.browser.find_element_by_id("password")
#         password.send_keys(PASSWORD)
#         password.send_keys(Keys.ENTER)
#         # self.wait_for_element("welcome-user", username)

#     def create_app(self):
#         self.client = app.test_client()
#         db.session.close()
#         db.drop_all()
#         db.create_all()
#         return app

#     def setUp(self):
#         self.app = self.create_app()
#         self.browser = webdriver.Chrome()

#     def tearDown(self):
#         self.browser.quit()

#     def test_navigation_when_logged_in(self):
#         self.browser.get(self.get_server_url())
#         nav = self.browser.find_element_by_id('nav-home').find_element_by_xpath(".//a")
#         assert url_for('index') in nav.get_attribute('href')
#         nav = self.browser.find_element_by_id('nav-login').find_element_by_xpath(".//a")
#         assert url_for('login') in nav.get_attribute('href')