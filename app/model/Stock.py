from dataclasses import dataclass, astuple
from datetime import datetime

@dataclass
class Stock:
    product_id: int 
    amount: str
    created_at: datetime
    updated_at: datetime

    def load(self):
        return astuple(self)
