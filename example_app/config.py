"""Configuration module."""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration."""

    DEBUG = True
    AWS_REGION = "us-west-2"
    DYNAMODB_TABLE = "graviton2-gh-runner-flask-app"
    DYNAMODB_KWARGS = {
        "region_name": AWS_REGION,
    }

    @staticmethod
    def init_app(app):
        pass


class Test(Config):
    """Testing configuration."""


class Development(Config):
    """Development configuration."""

    AWS_REGION = "us-west-2"
    DYNAMODB_KWARGS = {
        "endpoint_url": "http://localhost:8000",
        "region_name": AWS_REGION,
    }


class Staging(Config):
    """Staging configuration."""


class Production(Config):
    """Production configuration."""

    DEBUG = False


config = {
    "development": Development,
    "staging": Staging,
    "production": Production,
    "test": Test,
}
