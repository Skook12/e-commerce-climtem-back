from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Stock:
    product_id: int = field(init=False)
    amount: str
    created_at: datetime
    updated_at: datetime
    def load(self):
        return (
            self.amount,
            self.datetime,
            f'{self.created_at}',
            f'{self.updated_at}'
        )
