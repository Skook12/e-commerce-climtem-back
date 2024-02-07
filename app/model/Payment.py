from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Payment:
    id: int = field(init=False)
    order_id: int = field(init=False)
    type: str
    deadline: datetime
