"""Local data loader."""

import random
import uuid
from decimal import Decimal
from typing import List

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
from graviton2_gh_runner_flask_app.models.cart_model import CartItem, Cart
from graviton2_gh_runner_flask_app.models.orders_model import Order, OrderItem

app = create_app("development")


def load_book_data(app, book_ids: List[str]):
    """Generate 25 fake books."""
    book_controller: BookController = app.extensions["books_controller"]
    genre_choices = [
        "comedy",
        "sci-fi",
        "autobiography",
        "mystery",
        "thriller",
    ]

    for book_id in book_ids:
        b = Book(
            book_id=book_id,
            author="A. Uthor",
            genre=random.choice(genre_choices),
            rating=Decimal(5),
        )

        book_controller.put_new_book(item=b.record)


def create_cart_data(app, user_ids: List[str], book_ids: List[str]):
    """Create a cart for each user with 5 items in it."""
    cart_controller: CartController = app.extensions["cart_controller"]

    for user_id in user_ids:
        for _ in range(0, 5):
            c = CartItem(
                user_id=user_id,
                cart_item_id=str(uuid.uuid4()),
                item_id=random.choice(book_ids),
                item_cost=Decimal("10.99"),
                item_count=Decimal("1"),
            )

            cart_controller.put_cart_item(item=c.record)


def load_order_data(app, user_ids: List[str], book_ids: List[str]):
    """Generate 5 fake users, each with 5 orders."""
    order_controller: OrderController = app.extensions["orders_controller"]

    for user_id in user_ids:
        # Generate 5 orders per user
        for _ in range(0, 5):
            o = Order(
                user_id=user_id,
                order_id=str(uuid.uuid4()),
                total=Decimal("34.99"),
                shipping_address="3 Abbey Rd, London NW8 9AY, United Kingdom",
                billing_address="3 Abbey Rd, London NW8 9AY, United Kingdom",
                order_date="2021-07-12",
                ship_date="2021-07-14",
                items=[
                    OrderItem(
                        item_id=random.choice(book_ids),
                        price=Decimal("10.99"),
                        item_count=Decimal("2"),
                    ),
                    OrderItem(
                        item_id=random.choice(book_ids),
                        price=Decimal("13.01"),
                        item_count=Decimal("1"),
                    ),
                ],
            )

            order_controller.put_new_order(item=o.record)


if __name__ == "__main__":
    book_ids = [str(uuid.uuid4()) for _ in range(0, 25)]
    user_ids = [str(uuid.uuid4()) for _ in range(0, 5)]
    print(f"User IDs: {user_ids}")
    load_book_data(app=app, book_ids=book_ids)
    load_order_data(app=app, user_ids=user_ids, book_ids=book_ids)
    create_cart_data(app=app, user_ids=user_ids, book_ids=book_ids)
