from flask import Flask
import os
import tempfile
import pytest
from app import app, db
from selenium import webdriver
from flask_testing import LiveServerTestCase


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
