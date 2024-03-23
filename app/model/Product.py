from dataclasses import dataclass, field

@dataclass
class Product:
    brand_id: int
    category_id: int
    name: str
    description: str
    value: float
    discount: float

    def load(self):
        return (
            self.brand_id,
            self.category_id,
            self.name,
            self.description,
            self.value,
            self.discount
        )
