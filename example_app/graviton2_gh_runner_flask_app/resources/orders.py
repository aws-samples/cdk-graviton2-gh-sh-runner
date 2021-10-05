"""Cart resource for API."""

from flask import current_app
from flask.views import MethodView

from botocore.client import ClientError  # type: ignore

from ..controllers.orders_controller import OrderController
from ..helpers.helpers import convert_decimal


class OrdersView(MethodView):
    """View for retrieving all and creating orders for the given user."""

    def __init__(self) -> None:
        super().__init__()
        self.order: OrderController = current_app.extensions[
            "orders_controller"
        ]

    def get(self, user_id: str):
        """Get the current cart (exclusive of items).

        Args:
            user_id: the id of the user whose cart we are retreiving
        """
        try:
            data = self.order.get_all_user_orders(user_id=user_id)
        except ClientError as e:
            resp = {"error": str(e)}, 404
        else:
            resp = {"data": convert_decimal(data.get("Items"))}, 200

        return resp


class OrderView(MethodView):
    """View for CRUD'ing on an order."""

    def __init__(self) -> None:
        super().__init__()
        self.order: OrderController = current_app.extensions[
            "orders_controller"
        ]

    def get(self, user_id: str, order_id: str):
        """Get all items in a shopping cart.

        Args:
            user_id: the id of the user whose cart we are retreiving
        """
        try:
            data = self.order.get_order(user_id=user_id, order_id=order_id)
        except ClientError as e:
            resp = {"error": str(e)}, 404
        else:
            resp = {"data": convert_decimal(data.get("Item", {}))}, 200

        return resp
