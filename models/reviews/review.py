from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Review:
    customer_id: int
    product_id: int
    rating: float
    comment: Optional[str] = None

    def __post_init__(self):
        if not (1<=self.rating <=5):
            raise ValueError("Rating must be between 1 and 5")

    def to_row(self):
        return {
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "rating": self.rating,
            "comment": self.comment,
        }

    def __str__(self):
        stars ="*" * int(self.rating)
        return f"Review({self.customer_id} - {self.product_id}: {stars}), {self.comment})"