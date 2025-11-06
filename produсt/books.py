from dataclasses import dataclass
from typing import Dict, Any
from product import Product


@dataclass
class Book(Product):
    author: str
    page_count: int

    def to_row(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "weight": self.weight,
            "category": "book",
            "author": self.author,
            "page_count": self.page_count,
        }
