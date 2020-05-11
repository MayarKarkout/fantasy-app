from flask import Flask
from flask_testing import TestCase
from config import TestConfig
from app import create_app, db

class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        # create_app(TestConfig)
        # pass in test configuration
        return create_app(TestConfig)

    def setUp(self):

        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()