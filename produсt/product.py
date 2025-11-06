from abc import ABC, abstractmethod  # ABC = Abstract Base Class
from dataclasses import dataclass  # @dataclass automatically creates __init__, __repr__, etc.
from typing import Optional, Dict, Any  # typing hints: Optional means “can be None”


@dataclass
class Product(ABC):
    """Abstract base class for all product types."""

    id: Optional[int]  # id = None initially; MySQL will create it automatically via AUTO_INCREMENT
    name: str
    price: float
    weight: float

    @abstractmethod
    def to_row(self) -> Dict[str, Any]:
        """
        Return a dictionary of all fields.
        Must be overridden in every subclass.
        Used later for database INSERT or UPDATE operations.
        """
        pass
