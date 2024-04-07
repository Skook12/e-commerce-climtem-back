from dataclasses import dataclass, field, astuple
from datetime import datetime

@dataclass
class Order:
    user_id: int
    buy_date: datetime
    status: str
    
    def load(self):
        return astuple(self)