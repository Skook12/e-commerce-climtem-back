from dataclasses import dataclass, field

@dataclass
class Category:
    id: int = field(init=False)
    product_id: int = field(init=False)
    name: str
