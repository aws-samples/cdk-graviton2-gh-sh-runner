"""Book resource for API."""

from flask import current_app, request
from flask.views import MethodView

from botocore.client import ClientError  # type: ignore

from ..controllers.books_controller import BookController
from ..models.books_model import Book
from ..helpers.helpers import convert_decimal


class BookView(MethodView):
    """View for retrieving all books and adding new books."""

    def __init__(self) -> None:
        super().__init__()
        self.books_controller: BookController = current_app.extensions[
            "books_controller"
        ]

    def get(self):
        """Get all books from the data store."""
        try:
            data = self.books_controller.get_all_books()
        except ClientError as e:
            resp = {"error": str(e)}, 404
        else:
            resp = {"data": convert_decimal(data.get("Items"))}, 200

        return resp

    def post(self):
        """Add a new book."""
        body = request.get_json()

        if body:
            b = Book(**body)

            try:
                self.books_controller.put_new_book(item=b.record)
            except ClientError as e:
                resp = {"error": str(e)}, 404
            else:
                resp = {"data": b.book_id}, 201
        else:
            resp = {"error": "missing body"}, 404

        return resp


class SingleBookView(MethodView):
    """View for CRUD'ing on a single book."""

    def __init__(self) -> None:
        super().__init__()
        self.books_controller: BookController = current_app.extensions[
            "books_controller"
        ]

    def get(self, book_id: str):
        """Get a single book from the data store.

        Args:
            book_id: str - the id of a book
        """
        try:
            data = self.books_controller.get_book(book_id=book_id)
        except ClientError as e:
            resp = {"error": str(e)}, 404
        else:
            resp = {"data": convert_decimal(data.get("Item"))}, 200

        return resp
