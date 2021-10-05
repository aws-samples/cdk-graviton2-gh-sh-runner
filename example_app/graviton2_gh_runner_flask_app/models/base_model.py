"""Base model."""

import json

from .helpers import DecimalEncoder


class BaseModel:
    """Base module upon which all other models are built."""

    def deserialize(self):
        """Return a json safe string that covers decimals to floats or ints."""
        return json.dumps(self.record, cls=DecimalEncoder)
