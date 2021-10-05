"""Fake products svc."""

from flask import Flask

from config import config

# Import models
from .controllers.books_controller import BookController
from .controllers.cart_controller import CartController
from .controllers.orders_controller import OrderController
from .dynamodb.context_manager import DynamoConnectionManager


def create_app(env_config):
    """Application factory."""

    app = Flask(__name__)
    app.config.from_object(config[env_config])

    # DynamoClient
    dynamo = DynamoConnectionManager()
    dynamo.init_app(app=app)

    # Controllers
    book_controller = BookController(connection_manager=dynamo)
    cart_controller = CartController(connection_manager=dynamo)
    order_controller = OrderController(connection_manager=dynamo)
    book_controller.init_app(app=app)
    cart_controller.init_app(app=app)
    order_controller.init_app(app=app)

    # Import views
    from .resources.books import BookView, SingleBookView
    from .resources.cart import CartView, CartItemsView
    from .resources.orders import OrderView, OrdersView

    # Add views
    books = BookView.as_view("books")
    single_book = SingleBookView.as_view("single_book")
    cart = CartView.as_view("cart")
    cart_items = CartItemsView.as_view("cart_items")
    orders = OrdersView.as_view("orders")
    order = OrderView.as_view("order")

    # Add url rules for views
    app.add_url_rule(
        "/books", view_func=books, methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/books/<book_id>", view_func=single_book, methods=["GET"],
    )
    app.add_url_rule(
        "/cart/<user_id>", view_func=cart, methods=["GET"],
    )
    app.add_url_rule(
        "/cart/<user_id>/items", view_func=cart_items, methods=["GET"],
    )
    app.add_url_rule(
        "/orders/<user_id>", view_func=orders, methods=["GET"],
    )
    app.add_url_rule(
        "/orders/<user_id>/order/<order_id>", view_func=order, methods=["GET"],
    )

    return app
