"""Cart resource for API."""

from flask import current_app
from flask.views import MethodView

from botocore.client import ClientError  # type: ignore

from ..controllers.cart_controller import CartController
from ..helpers.helpers import convert_decimal


class CartView(MethodView):
    """View for retrieving metadata about the current cart."""

    def __init__(self) -> None:
        super().__init__()
        self.cart_controller: CartController = current_app.extensions[
            "cart_controller"
        ]

    def get(self, user_id: str):
        """Get the current cart (exclusive of items).

        Args:
            user_id: the id of the user whose cart we are retreiving
        """
        try:
            data = self.cart_controller.get_cart(user_id=user_id)
        except ClientError as e:
            resp = {"error": str(e)}, 404
        else:
            resp = {"data": convert_decimal(data.get("Item", {}))}, 200

        return resp


class CartItemsView(MethodView):
    """View for CRUD'ing on a single book."""

    def __init__(self) -> None:
        super().__init__()
        self.cart_controller: CartController = current_app.extensions[
            "cart_controller"
        ]

    def get(self, user_id: str):
        """Get all items in a shopping cart.

        Args:
            user_id: the id of the user whose cart we are retreiving
        """
        try:
            data = self.cart_controller.get_cart_items(user_id=user_id)
        except ClientError as e:
            resp = {"error": str(e)}, 404
        else:
            resp = {"data": convert_decimal(data.get("Items"))}, 200

        return resp
