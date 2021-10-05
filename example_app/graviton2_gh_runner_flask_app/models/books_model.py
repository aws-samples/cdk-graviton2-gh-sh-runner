"""Model for Books."""

from decimal import Decimal
from dataclasses import dataclass

from .base_model import BaseModel


@dataclass
class Book(BaseModel):
    book_id: str
    author: str
    genre: str
    rating: Decimal

    @property
    def pk(self):
        """Primary key."""
        return f"book_id#{self.book_id}"

    @property
    def sk(self):
        """Sort key."""
        return f"book_id#{self.book_id}"

    @property
    def gsi1_pk(self):
        """Primary key for Global Secondary Index."""
        return "data_type#book"

    @property
    def gsi1_sk(self):
        """Primary key."""
        return f"book_id#{self.book_id}"

    @property
    def record(self):
        """Serialize the record."""
        item = {
            "pk": self.pk,
            "sk": self.sk,
            "gsi1_pk": self.gsi1_pk,
            "gsi1_sk": self.gsi1_sk,
        }

        item.update(self.__dict__)

        return item
