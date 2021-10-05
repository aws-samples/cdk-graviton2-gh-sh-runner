"""Model for Cart."""

from decimal import Decimal
from dataclasses import dataclass

from .base_model import BaseModel


@dataclass
class Cart(BaseModel):
    user_id: str
    item_count: Decimal
    total: Decimal

    @property
    def pk(self):
        """Primary key."""
        return f"user_id#{self.user_id}"

    @property
    def sk(self):
        """Sort key."""
        return f"cart#{self.user_id}"

    @property
    def record(self):
        """Serialize the record."""
        item = {
            "pk": self.pk,
            "sk": self.sk,
        }

        item.update(self.__dict__)

        return item


@dataclass
class CartItem(BaseModel):
    user_id: str
    cart_item_id: str
    item_id: str
    item_cost: Decimal
    item_count: Decimal

    @property
    def pk(self):
        """Primary key."""
        return f"user_id#{self.user_id}"

    @property
    def sk(self):
        """Sort key."""
        return f"cart#{self.user_id}+item#{self.cart_item_id}"

    @property
    def record(self):
        """Serialize the record."""
        item = {
            "pk": self.pk,
            "sk": self.sk,
        }

        item.update(self.__dict__)

        return item
