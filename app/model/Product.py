from dataclasses import dataclass, astuple

@dataclass
class Product:
    brand_id: int
    category_id: int
    name: str
    description: str
    value: float
    discount: float
    highl: bool

    def load(self):
        return astuple(self)

@dataclass
class Image:
    product_id: int
    path: str
    
    def load(self):
        return astuple(self)
