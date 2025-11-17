from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Product(ABC):
    """
    Abstract base class for all product types.
    Matches SQL table `product`.
    """

    product_id: Optional[int]   # None → DB AUTO_INCREMENT
    product: str                # назва товару
    price: float
    weight: float
    category: str               # electronics | clothing | books

    @abstractmethod
    def to_row(self) -> Dict[str, Any]:
        """
        Must return dict matching SQL columns for INSERT/UPDATE:
        {
            "product_id": ...,
            "product": ...,
            "price": ...,
            "weight": ...,
            "category": ...
        }
        Subclasses must extend it with category-specific fields
        (brand, author, size, ...).
        """
        pass
