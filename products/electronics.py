from dataclasses import dataclass
from typing import Dict, Any
from product import Product


@dataclass
class Electronics(Product):
    brand: str
    warranty_years: int

    def to_row(self) -> Dict[str, Any]:
        return {
            "product_id": self.product_id,
            "product": self.product,
            "price": self.price,
            "weight": self.weight,
            "category": self.category,
            "brand": self.brand,
            "warranty_years": self.warranty_years,
        }
