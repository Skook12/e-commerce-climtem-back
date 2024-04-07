from dataclasses import dataclass, astuple

@dataclass
class Product:
    brand_id: int
    category_id: int
    name: str
    description: str
    value: float
    discount: float

    def load(self):
        return astuple(self)
