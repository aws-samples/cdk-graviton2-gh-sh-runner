"""Base model class."""

import boto3  # type: ignore


class DynamoConnectionManager:
    def __init__(self, app=None):
        """."""
        self.app = app
        self._connection = None
        self._table = None

        if app is not None:
            self.init_app(app)

            self._connection = boto3.resource(
                "dynamodb", **app.config.get("DYNAMODB_KWARGS")
            )
            self._table = self._connection.Table(
                app.config.get("DYNAMODB_TABLE"),
            )

    def init_app(self, app):
        """Initialize the extension."""

        self._connection = boto3.resource(
            "dynamodb", **app.config.get("DYNAMODB_KWARGS")
        )
        self._table = self._connection.Table(app.config.get("DYNAMODB_TABLE"))

        app.extensions["dynamodb"] = self

    @property
    def table(self):
        """."""
        return self._table
