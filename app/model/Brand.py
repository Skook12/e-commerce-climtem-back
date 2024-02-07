from dataclasses import dataclass, field

@dataclass
class Brand:
    id: int = field(init=False)
    product_id: int = field(init=False)
    name: str
