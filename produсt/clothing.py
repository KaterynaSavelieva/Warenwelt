from dataclasses import dataclass
from typing import Dict, Any
from product import Product


@dataclass
class Clothing(Product):
    size: str

    def to_row(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "weight": self.weight,
            "category": "clothing",
            "size": self.size,
        }
