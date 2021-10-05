"""Controller for books models."""

from boto3.dynamodb.conditions import Key  # type: ignore

from ..dynamodb.context_manager import DynamoConnectionManager


class BookController:
    """."""

    def __init__(self, connection_manager: DynamoConnectionManager, app=None):
        """."""
        self.app = app
        self.table_connection = connection_manager.table

        if app is not None:
            self.init_app(app)

            self.table_connection = connection_manager.table

    def init_app(self, app=None):
        """Initialize the app with this extension. Used by the app factory."""
        app.extensions["books_controller"] = self

    def put_new_book(self, item: dict):
        """Add a new book to DynamoDB."""
        return self.table_connection.put_item(Item=item)

    def get_all_books(self):
        """Get all books from DynamoDB."""
        return self.table_connection.query(
            IndexName="gsi1",
            KeyConditionExpression=Key("gsi1_pk").eq("data_type#book")
            & Key("gsi1_sk").begins_with("book_id#"),
        )

    def get_book(self, book_id: str):
        """Get a single book from DynamoDB."""
        return self.table_connection.get_item(
            Key={"pk": f"book_id#{book_id}", "sk": f"book_id#{book_id}"}
        )
