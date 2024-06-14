from dataclasses import dataclass, astuple

@dataclass
class Product:
    ID_Brand: int
    ID_Category: int
    name: str
    description: str
    value: float
    discount: float
    highl: bool
    quantity: int

    def load(self):
        return astuple(self)

@dataclass
class Image:
    product_id: int
    path: str
    
    def load(self):
        return astuple(self)
