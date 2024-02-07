from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Order:
    id: int = field(init=False)
    User_id: int = field(init=False)
    buy_date: datetime
    status: str