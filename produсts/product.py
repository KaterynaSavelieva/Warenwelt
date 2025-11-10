from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Product(ABC):
    """Abstract base class for all product types (matches SQL schema)."""

    product_id: Optional[int]  # None for new rows; DB assigns AUTO_INCREMENT
    product: str
    price: float
    weight: float

    @abstractmethod
    def to_row(self) -> Dict[str, Any]:
        """
        Return a dictionary of all fields (keys must match SQL column names),
        e.g. include 'product_id', 'name', 'price', 'weight', 'category', ...
        """
        pass
