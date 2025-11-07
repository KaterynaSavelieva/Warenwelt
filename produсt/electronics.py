from dataclasses import dataclass
from typing import Dict, Any
from product import Product


@dataclass
class Electronics(Product):
    brand: str
    warranty_years: int

    def to_row(self) -> Dict[str, Any]:
        return {
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "weight": self.weight,
            "category": "electronics",
            "brand": self.brand,
            "warranty_years": self.warranty_years
        }
