from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Stock:
    id: int = field(init=False)
    product_id: int = field(init=False)
    amount: str
    created_at: datetime
    updated_at: datetime