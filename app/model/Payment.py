from dataclasses import dataclass, field, astuple
from datetime import datetime

@dataclass
class Payment:
    order_id: int = field(init=False)
    type: str
    deadline: datetime

    def load(self):
        return astuple(self)