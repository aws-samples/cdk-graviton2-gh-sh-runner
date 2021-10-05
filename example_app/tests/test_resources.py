"""Unit tests for resources."""

import pytest

from botocore.stub import Stubber

from graviton2_gh_runner_flask_app import create_app

app = create_app("test")


@pytest.fixture
def client():
    """Create a flask client that will be used by all future tests."""

    with app.test_client() as client:
        yield client


def test_books_get_all_books(client):
    """."""
    stubber = Stubber(app.extensions["dynamodb"].table.meta.client)

    stubber.add_response(
        "query",
        {
            "Items": [
                {
                    "pk": {
                        "S": "book_id#1d3e7061-c364-4966-bf39-dbe53f1377f8"
                    },
                    "sk": {
                        "S": "book_id#1d3e7061-c364-4966-bf39-dbe53f1377f8"
                    },
                    "book_id": {"S": "1d3e7061-c364-4966-bf39-dbe53f1377f8"},
                    "author": {"S": "A. Uthor"},
                    "genre": {"S": "sci-fi"},
                    "rating": {"N": "5"},
                    "gsi1_pk": {"S": "data_type#book"},
                    "gsi1_sk": {
                        "S": "book_id#1d3e7061-c364-4966-bf39-dbe53f1377f8"
                    },
                },
                {
                    "pk": {
                        "S": "book_id#b72638b8-1d08-43dc-813e-43e1341b4f09"
                    },
                    "sk": {
                        "S": "book_id#b72638b8-1d08-43dc-813e-43e1341b4f09"
                    },
                    "book_id": {"S": "b72638b8-1d08-43dc-813e-43e1341b4f09"},
                    "author": {"S": "A. Author"},
                    "genre": {"S": "comedy"},
                    "rating": {"N": "5"},
                    "gsi1_pk": {"S": "data_type#book"},
                    "gsi1_sk": {
                        "S": "book_id#b72638b8-1d08-43dc-813e-43e1341b4f09"
                    },
                },
            ]
        },
    )

    with stubber:
        rv = client.get("/books")
        assert rv.json == {
            "data": [
                {
                    "author": "A. Uthor",
                    "book_id": "1d3e7061-c364-4966-bf39-dbe53f1377f8",
                    "genre": "sci-fi",
                    "gsi1_pk": "data_type#book",
                    "gsi1_sk": "book_id#1d3e7061-c364-4966-bf39-dbe53f1377f8",
                    "pk": "book_id#1d3e7061-c364-4966-bf39-dbe53f1377f8",
                    "rating": 5,
                    "sk": "book_id#1d3e7061-c364-4966-bf39-dbe53f1377f8",
                },
                {
                    "author": "A. Author",
                    "book_id": "b72638b8-1d08-43dc-813e-43e1341b4f09",
                    "genre": "comedy",
                    "gsi1_pk": "data_type#book",
                    "gsi1_sk": "book_id#b72638b8-1d08-43dc-813e-43e1341b4f09",
                    "pk": "book_id#b72638b8-1d08-43dc-813e-43e1341b4f09",
                    "rating": 5,
                    "sk": "book_id#b72638b8-1d08-43dc-813e-43e1341b4f09",
                },
            ]
        }


def test_books_get_single_book(client):
    """."""
    stubber = Stubber(app.extensions["dynamodb"].table.meta.client)

    stubber.add_response(
        "get_item",
        {
            "Item": {
                "pk": {"S": "book_id#1d3e7061-c364-4966-bf39-dbe53f1377f8"},
                "sk": {"S": "book_id#1d3e7061-c364-4966-bf39-dbe53f1377f8"},
                "book_id": {"S": "1d3e7061-c364-4966-bf39-dbe53f1377f8"},
                "author": {"S": "A. Uthor"},
                "genre": {"S": "sci-fi"},
                "rating": {"N": "5"},
                "gsi1_pk": {"S": "data_type#book"},
                "gsi1_sk": {
                    "S": "book_id#1d3e7061-c364-4966-bf39-dbe53f1377f8"
                },
            }
        },
    )

    with stubber:
        rv = client.get("/books/1d3e7061-c364-4966-bf39-dbe53f1377f8")
        assert rv.json == {
            "data": {
                "author": "A. Uthor",
                "book_id": "1d3e7061-c364-4966-bf39-dbe53f1377f8",
                "genre": "sci-fi",
                "gsi1_pk": "data_type#book",
                "gsi1_sk": "book_id#1d3e7061-c364-4966-bf39-dbe53f1377f8",
                "pk": "book_id#1d3e7061-c364-4966-bf39-dbe53f1377f8",
                "rating": 5,
                "sk": "book_id#1d3e7061-c364-4966-bf39-dbe53f1377f8",
            }
        }


def test_get_cart_data(client):
    """."""
    stubber = Stubber(app.extensions["dynamodb"].table.meta.client)

    stubber.add_response(
        "get_item",
        {
            "Item": {
                "pk": {"S": "user_id#1fef09c7-5830-41b2-8b78-aa1c4933d9eb"},
                "sk": {"S": "cart#1fef09c7-5830-41b2-8b78-aa1c4933d9eb"},
                "user_id": {"S": "1fef09c7-5830-41b2-8b78-aa1c4933d9eb"},
                "item_count": {"N": "5"},
                "total": {"N": "50.99"},
            }
        },
    )

    with stubber:
        rv = client.get("/cart/1fef09c7-5830-41b2-8b78-aa1c4933d9eb")
        assert rv.json == {
            "data": {
                "item_count": 5,
                "pk": "user_id#1fef09c7-5830-41b2-8b78-aa1c4933d9eb",
                "sk": "cart#1fef09c7-5830-41b2-8b78-aa1c4933d9eb",
                "total": 50.99,
                "user_id": "1fef09c7-5830-41b2-8b78-aa1c4933d9eb",
            }
        }


def test_get_cart_items(client):
    """."""
    stubber = Stubber(app.extensions["dynamodb"].table.meta.client)

    stubber.add_response(
        "query",
        {
            "Items": [
                {
                    "pk": {
                        "S": "user_id#1fef09c7-5830-41b2-8b78-aa1c4933d9eb"
                    },
                    "sk": {
                        "S": "cart#1fef09c7-5830-41b2-8b78-aa1c4933d9eb+item#1ac27ce9-7877-4326-b211-57c41b65fcf4"
                    },
                    "user_id": {"S": "1fef09c7-5830-41b2-8b78-aa1c4933d9eb"},
                    "cart_item_id": {
                        "S": "1ac27ce9-7877-4326-b211-57c41b65fcf4"
                    },
                    "item_id": {"S": "2bb7c11f-29bf-4437-8a63-8ea01cf707c4"},
                    "item_cost": {"N": "10.99"},
                    "item_count": {"N": "2"},
                },
                {
                    "pk": {
                        "S": "user_id#1fef09c7-5830-41b2-8b78-aa1c4933d9eb"
                    },
                    "sk": {
                        "S": "cart#1fef09c7-5830-41b2-8b78-aa1c4933d9eb+item#890c4807-c004-4f96-80aa-fc7526e8655c"
                    },
                    "user_id": {"S": "1fef09c7-5830-41b2-8b78-aa1c4933d9eb"},
                    "cart_item_id": {
                        "S": "890c4807-c004-4f96-80aa-fc7526e8655c"
                    },
                    "item_id": {"S": "3a831010-519b-45b3-b6f6-9508f606faa1"},
                    "item_cost": {"N": "10.99"},
                    "item_count": {"N": "2"},
                },
            ]
        },
    )

    with stubber:
        rv = client.get("/cart/1fef09c7-5830-41b2-8b78-aa1c4933d9eb/items")
        assert rv.json == {
            "data": [
                {
                    "cart_item_id": "1ac27ce9-7877-4326-b211-57c41b65fcf4",
                    "item_cost": 10.99,
                    "item_count": 2,
                    "item_id": "2bb7c11f-29bf-4437-8a63-8ea01cf707c4",
                    "pk": "user_id#1fef09c7-5830-41b2-8b78-aa1c4933d9eb",
                    "sk": "cart#1fef09c7-5830-41b2-8b78-aa1c4933d9eb+item#1ac27ce9-7877-4326-b211-57c41b65fcf4",
                    "user_id": "1fef09c7-5830-41b2-8b78-aa1c4933d9eb",
                },
                {
                    "cart_item_id": "890c4807-c004-4f96-80aa-fc7526e8655c",
                    "item_cost": 10.99,
                    "item_count": 2,
                    "item_id": "3a831010-519b-45b3-b6f6-9508f606faa1",
                    "pk": "user_id#1fef09c7-5830-41b2-8b78-aa1c4933d9eb",
                    "sk": "cart#1fef09c7-5830-41b2-8b78-aa1c4933d9eb+item#890c4807-c004-4f96-80aa-fc7526e8655c",
                    "user_id": "1fef09c7-5830-41b2-8b78-aa1c4933d9eb",
                },
            ]
        }


def test_get_orders(client):
    """Test getting all orders for a user."""
    stubber = Stubber(app.extensions["dynamodb"].table.meta.client)

    stubber.add_response(
        "query",
        {
            "Items": [
                {
                    "pk": {
                        "S": "user_id#1fef09c7-5830-41b2-8b78-aa1c4933d9eb"
                    },
                    "sk": {
                        "S": "order_id#c817d12d-beb6-470a-b1b1-d25b5586413a"
                    },
                    "user_id": {"S": "1fef09c7-5830-41b2-8b78-aa1c4933d9eb"},
                    "order_id": {"S": "c817d12d-beb6-470a-b1b1-d25b5586413a"},
                    "total": {"N": "50.99"},
                    "shipping_address": {
                        "S": "3 Abbey Rd, London NW8 9AY, United Kingdom"
                    },
                    "billing_address": {
                        "S": "3 Abbey Rd, London NW8 9AY, United Kingdom"
                    },
                    "order_date": {"S": "2021-07-12"},
                    "ship_date": {"S": "2021-07-14"},
                    "items": {
                        "L": [
                            {
                                "M": {
                                    "item_id": {
                                        "S": "73191601-686a-4b5c-9070-adfba42a1d89"
                                    },
                                    "price": {"N": "4"},
                                    "item_count": {"N": "10.99"},
                                }
                            },
                            {
                                "M": {
                                    "item_id": {
                                        "S": "2c23bcd0-904d-4ffd-a8a0-75ad932cd3b9"
                                    },
                                    "price": {"N": "1"},
                                    "item_count": {"N": "7.03"},
                                }
                            },
                        ]
                    },
                },
                {
                    "pk": {
                        "S": "user_id#1fef09c7-5830-41b2-8b78-aa1c4933d9eb"
                    },
                    "sk": {
                        "S": "order_id#8197378d-140b-4c97-81af-1ab8cbd05d0b"
                    },
                    "user_id": {"S": "1fef09c7-5830-41b2-8b78-aa1c4933d9eb"},
                    "order_id": {"S": "8197378d-140b-4c97-81af-1ab8cbd05d0b"},
                    "total": {"N": "50.99"},
                    "shipping_address": {
                        "S": "3 Abbey Rd, London NW8 9AY, United Kingdom"
                    },
                    "billing_address": {
                        "S": "3 Abbey Rd, London NW8 9AY, United Kingdom"
                    },
                    "order_date": {"S": "2021-07-12"},
                    "ship_date": {"S": "2021-07-14"},
                    "items": {
                        "L": [
                            {
                                "M": {
                                    "item_id": {
                                        "S": "e5cedce0-6002-438d-850a-60b516e5e3a7"
                                    },
                                    "price": {"N": "3"},
                                    "item_count": {"N": "10.99"},
                                }
                            },
                            {
                                "M": {
                                    "item_id": {
                                        "S": "1dd39c17-379b-4739-a930-5f57959ac52e"
                                    },
                                    "price": {"N": "2"},
                                    "item_count": {"N": "9.01"},
                                }
                            },
                        ]
                    },
                },
            ]
        },
    )

    with stubber:
        rv = client.get("/orders/1fef09c7-5830-41b2-8b78-aa1c4933d9eb")
        assert rv.json == {
            "data": [
                {
                    "billing_address": "3 Abbey Rd, London NW8 9AY, United Kingdom",
                    "items": [
                        {
                            "item_count": 10.99,
                            "item_id": "73191601-686a-4b5c-9070-adfba42a1d89",
                            "price": 4,
                        },
                        {
                            "item_count": 7.03,
                            "item_id": "2c23bcd0-904d-4ffd-a8a0-75ad932cd3b9",
                            "price": 1,
                        },
                    ],
                    "order_date": "2021-07-12",
                    "order_id": "c817d12d-beb6-470a-b1b1-d25b5586413a",
                    "pk": "user_id#1fef09c7-5830-41b2-8b78-aa1c4933d9eb",
                    "ship_date": "2021-07-14",
                    "shipping_address": "3 Abbey Rd, London NW8 9AY, United Kingdom",
                    "sk": "order_id#c817d12d-beb6-470a-b1b1-d25b5586413a",
                    "total": 50.99,
                    "user_id": "1fef09c7-5830-41b2-8b78-aa1c4933d9eb",
                },
                {
                    "billing_address": "3 Abbey Rd, London NW8 9AY, United Kingdom",
                    "items": [
                        {
                            "item_count": 10.99,
                            "item_id": "e5cedce0-6002-438d-850a-60b516e5e3a7",
                            "price": 3,
                        },
                        {
                            "item_count": 9.01,
                            "item_id": "1dd39c17-379b-4739-a930-5f57959ac52e",
                            "price": 2,
                        },
                    ],
                    "order_date": "2021-07-12",
                    "order_id": "8197378d-140b-4c97-81af-1ab8cbd05d0b",
                    "pk": "user_id#1fef09c7-5830-41b2-8b78-aa1c4933d9eb",
                    "ship_date": "2021-07-14",
                    "shipping_address": "3 Abbey Rd, London NW8 9AY, United Kingdom",
                    "sk": "order_id#8197378d-140b-4c97-81af-1ab8cbd05d0b",
                    "total": 50.99,
                    "user_id": "1fef09c7-5830-41b2-8b78-aa1c4933d9eb",
                },
            ]
        }


def test_get_order(client):
    """Test getting a single order."""
    stubber = Stubber(app.extensions["dynamodb"].table.meta.client)

    stubber.add_response(
        "get_item",
        {
            "Item": {
                "pk": {"S": "user_id#1fef09c7-5830-41b2-8b78-aa1c4933d9eb"},
                "sk": {"S": "order_id#c817d12d-beb6-470a-b1b1-d25b5586413a"},
                "user_id": {"S": "1fef09c7-5830-41b2-8b78-aa1c4933d9eb"},
                "order_id": {"S": "c817d12d-beb6-470a-b1b1-d25b5586413a"},
                "total": {"N": "50.99"},
                "shipping_address": {
                    "S": "3 Abbey Rd, London NW8 9AY, United Kingdom"
                },
                "billing_address": {
                    "S": "3 Abbey Rd, London NW8 9AY, United Kingdom"
                },
                "order_date": {"S": "2021-07-12"},
                "ship_date": {"S": "2021-07-14"},
                "items": {
                    "L": [
                        {
                            "M": {
                                "item_id": {
                                    "S": "73191601-686a-4b5c-9070-adfba42a1d89"
                                },
                                "price": {"N": "4"},
                                "item_count": {"N": "10.99"},
                            }
                        },
                        {
                            "M": {
                                "item_id": {
                                    "S": "2c23bcd0-904d-4ffd-a8a0-75ad932cd3b9"
                                },
                                "price": {"N": "1"},
                                "item_count": {"N": "7.03"},
                            }
                        },
                    ]
                },
            }
        },
    )

    with stubber:
        rv = client.get(
            "/orders/1fef09c7-5830-41b2-8b78-aa1c4933d9eb/order/c817d12d-beb6-470a-b1b1-d25b5586413a"
        )
        assert rv.json == {
            "data": {
                "billing_address": "3 Abbey Rd, London NW8 9AY, United Kingdom",
                "items": [
                    {
                        "item_count": 10.99,
                        "item_id": "73191601-686a-4b5c-9070-adfba42a1d89",
                        "price": 4,
                    },
                    {
                        "item_count": 7.03,
                        "item_id": "2c23bcd0-904d-4ffd-a8a0-75ad932cd3b9",
                        "price": 1,
                    },
                ],
                "order_date": "2021-07-12",
                "order_id": "c817d12d-beb6-470a-b1b1-d25b5586413a",
                "pk": "user_id#1fef09c7-5830-41b2-8b78-aa1c4933d9eb",
                "ship_date": "2021-07-14",
                "shipping_address": "3 Abbey Rd, London NW8 9AY, United Kingdom",
                "sk": "order_id#c817d12d-beb6-470a-b1b1-d25b5586413a",
                "total": 50.99,
                "user_id": "1fef09c7-5830-41b2-8b78-aa1c4933d9eb",
            }
        }

