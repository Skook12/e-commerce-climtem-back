from dataclasses import dataclass, field

@dataclass
class Product:
    id: int = field(init=False)
    name: str
    description: str
    value: float
    discount: float
