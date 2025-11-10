from dataclasses import dataclass
from typing import Dict, Any
from product import Product


@dataclass
class Clothing(Product):
    size: str

    def to_row(self) -> Dict[str, Any]:
        return {
            "product_id": self.product_id,
            "product": self.product,
            "price": self.price,
            "weight": self.weight,
            "category": "clothing",
            "size": self.size,
        }
