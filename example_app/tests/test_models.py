"""Test all models."""

from decimal import Decimal

import pytest
from botocore.stub import Stubber
from botocore.client import ClientError

from graviton2_gh_runner_flask_app import create_app
from graviton2_gh_runner_flask_app.controllers.books_controller import (
    BookController,
)
from graviton2_gh_runner_flask_app.controllers.cart_controller import (
    CartController,
)
from graviton2_gh_runner_flask_app.controllers.orders_controller import (
    OrderController,
)
from graviton2_gh_runner_flask_app.models.books_model import Book
from graviton2_gh_runner_flask_app.models.cart_model import CartItem
from graviton2_gh_runner_flask_app.models.orders_model import Order, OrderItem

app = create_app("test")


@pytest.fixture
def client():
    """Create a flask client that will be used by all future tests."""

    with app.test_client() as client:
        yield client


def test_create_book_instance():
    """Test creating a book model."""
    b = Book(
        book_id="de1abcc4-e737-44d3-8a96-b76d12841b26",
        author="A. Uthor",
        genre="comedy",
        rating=Decimal(5),
    )

    assert b.record == {
        "pk": "book_id#de1abcc4-e737-44d3-8a96-b76d12841b26",
        "sk": "book_id#de1abcc4-e737-44d3-8a96-b76d12841b26",
        "gsi1_pk": "data_type#book",
        "gsi1_sk": "book_id#de1abcc4-e737-44d3-8a96-b76d12841b26",
        "book_id": "de1abcc4-e737-44d3-8a96-b76d12841b26",
        "author": "A. Uthor",
        "genre": "comedy",
        "rating": Decimal("5"),
    }


def test_book_put_success():
    """Test creating a book model."""
    stubber = Stubber(app.extensions["dynamodb"].table.meta.client)
    book_controller: BookController = app.extensions["books_controller"]

    b = Book(
        book_id="de1abcc4-e737-44d3-8a96-b76d12841b26",
        author="A. Uthor",
        genre="comedy",
        rating=Decimal(5),
    )

    stubber.add_response("put_item", {})

    with stubber:
        try:
            book_controller.put_new_book(item=b.record)
        except ClientError as e:
            pytest.fail("Exception raised by DynamoDB PutItem: " + str(e))


#  Orders
def test_create_order_instance():
    """Test creating a book model."""
    o = Order(
        user_id="5f604681-5d73-413d-9bdc-282959d9c620",
        order_id="4f56023d-5435-4608-ab86-31ffbb4ee90b",
        total=Decimal("34.99"),
        shipping_address="3 Abbey Rd, London NW8 9AY, United Kingdom",
        billing_address="3 Abbey Rd, London NW8 9AY, United Kingdom",
        order_date="2021-07-12",
        ship_date="2021-07-14",
        items=[
            OrderItem(
                item_id="de1abcc4-e737-44d3-8a96-b76d12841b2",
                price=Decimal("10.99"),
                item_count=Decimal("2"),
            ),
            OrderItem(
                item_id="cd53d299-94ae-4d36-80b3-0deb40aaa5be",
                price=Decimal("13.01"),
                item_count=Decimal("1"),
            ),
        ],
    )

    assert o.record == {
        "pk": "user_id#5f604681-5d73-413d-9bdc-282959d9c620",
        "sk": "order_id#4f56023d-5435-4608-ab86-31ffbb4ee90b",
        "user_id": "5f604681-5d73-413d-9bdc-282959d9c620",
        "order_id": "4f56023d-5435-4608-ab86-31ffbb4ee90b",
        "total": Decimal("34.99"),
        "shipping_address": "3 Abbey Rd, London NW8 9AY, United Kingdom",
        "billing_address": "3 Abbey Rd, London NW8 9AY, United Kingdom",
        "order_date": "2021-07-12",
        "ship_date": "2021-07-14",
        "items": [
            {
                "item_id": "de1abcc4-e737-44d3-8a96-b76d12841b2",
                "price": Decimal("10.99"),
                "item_count": Decimal("2"),
            },
            {
                "item_id": "cd53d299-94ae-4d36-80b3-0deb40aaa5be",
                "price": Decimal("13.01"),
                "item_count": Decimal("1"),
            },
        ],
    }


def test_order_put_success():
    """Test creating a book model."""
    stubber = Stubber(app.extensions["dynamodb"].table.meta.client)
    order_controller: OrderController = app.extensions["orders_controller"]

    o = Order(
        user_id="5f604681-5d73-413d-9bdc-282959d9c620",
        order_id="4f56023d-5435-4608-ab86-31ffbb4ee90b",
        total=Decimal("34.99"),
        shipping_address="3 Abbey Rd, London NW8 9AY, United Kingdom",
        billing_address="3 Abbey Rd, London NW8 9AY, United Kingdom",
        order_date="2021-07-12",
        ship_date="2021-07-14",
        items=[
            OrderItem(
                item_id="de1abcc4-e737-44d3-8a96-b76d12841b2",
                price=Decimal("10.99"),
                item_count=Decimal("2"),
            ),
            OrderItem(
                item_id="cd53d299-94ae-4d36-80b3-0deb40aaa5be",
                price=Decimal("13.01"),
                item_count=Decimal("1"),
            ),
        ],
    )

    stubber.add_response("put_item", {})

    with stubber:
        try:
            order_controller.put_new_order(item=o.record)
        except ClientError as e:
            pytest.fail("Exception raised by DynamoDB PutItem: " + str(e))


# Cart
def test_create_cart_item():
    """Test adding an item to the cart."""
    c = CartItem(
        user_id="5f604681-5d73-413d-9bdc-282959d9c620",
        cart_item_id="bdd2a612-48f0-4970-9266-38191fde37b3",
        item_id="de1abcc4-e737-44d3-8a96-b76d12841b2",
        item_cost=Decimal("10.99"),
        item_count=Decimal("2"),
    )

    assert c.record == {
        "pk": "user_id#5f604681-5d73-413d-9bdc-282959d9c620",
        "sk": "cart#5f604681-5d73-413d-9bdc-282959d9c620+item#bdd2a612-48f0-4970-9266-38191fde37b3",
        "user_id": "5f604681-5d73-413d-9bdc-282959d9c620",
        "cart_item_id": "bdd2a612-48f0-4970-9266-38191fde37b3",
        "item_id": "de1abcc4-e737-44d3-8a96-b76d12841b2",
        "item_cost": Decimal("10.99"),
        "item_count": Decimal("2"),
    }


def test_put_cart_item():
    """Test creating a book model."""
    stubber = Stubber(app.extensions["dynamodb"].table.meta.client)
    cart_controller: CartController = app.extensions["cart_controller"]

    c = CartItem(
        user_id="5f604681-5d73-413d-9bdc-282959d9c620",
        cart_item_id="bdd2a612-48f0-4970-9266-38191fde37b3",
        item_id="de1abcc4-e737-44d3-8a96-b76d12841b2",
        item_cost=Decimal("10.99"),
        item_count=Decimal("2"),
    )
    stubber.add_response("put_item", {})

    with stubber:
        try:
            cart_controller.put_cart_item(item=c.record)
        except ClientError as e:
            pytest.fail("Exception raised by DynamoDB PutItem: " + str(e))
