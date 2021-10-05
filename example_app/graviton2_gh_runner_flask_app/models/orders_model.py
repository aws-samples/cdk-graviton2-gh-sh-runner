"""Model for Orders."""

from decimal import Decimal
from dataclasses import dataclass
from typing import List


from .base_model import BaseModel


@dataclass
class OrderItem(BaseModel):
    item_id: str
    price: Decimal
    item_count: Decimal

    @property
    def record(self):
        return self.__dict__


@dataclass
class Order(BaseModel):
    user_id: str
    order_id: str
    total: Decimal
    shipping_address: str
    billing_address: str
    order_date: str
    ship_date: str
    items: List[OrderItem]

    @property
    def pk(self):
        """Primary key."""
        return f"user_id#{self.user_id}"

    @property
    def sk(self):
        """Sort key."""
        return f"order_id#{self.order_id}"

    @property
    def record(self):
        """Serialize the record."""
        item = {
            "pk": self.pk,
            "sk": self.sk,
        }

        item.update(self.__dict__)

        item["items"] = [item.record for item in self.items]

        return item
