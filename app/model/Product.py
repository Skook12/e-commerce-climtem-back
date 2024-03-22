from dataclasses import dataclass, field

@dataclass
class Product:
    id: int = field(init=False)
    name: str
    description: str
    value: float
    discount: float
    def load(self):
        return (
            self.name,
            self.description,
            self.value,
            self.discount
        )
