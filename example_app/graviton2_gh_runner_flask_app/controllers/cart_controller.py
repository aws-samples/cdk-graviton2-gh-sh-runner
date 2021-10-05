"""Controller for cart model."""

from boto3.dynamodb.conditions import Key  # type: ignore

from ..dynamodb.context_manager import DynamoConnectionManager


class CartController:
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
        app.extensions["cart_controller"] = self

    def put_cart_item(self, item: dict):
        """ "Add a new item to the cart in DynamoDB."""
        return self.table_connection.put_item(Item=item)

    def get_cart_items(self, user_id: str):
        """."""
        return self.table_connection.query(
            KeyConditionExpression=Key("pk").eq(f"user_id#{user_id}")
            & Key("sk").begins_with(f"cart#{user_id}+item#")
        )

    def get_cart(self, user_id: str):
        """."""
        return self.table_connection.get_item(
            Key={"pk": f"user_id#{user_id}", "sk": f"cart#{user_id}"}
        )
