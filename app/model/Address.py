from dataclasses import dataclass, astuple
from typing import Optional

@dataclass
class Address:
    user_id: int
    number: int
    complement: Optional[str]
    cep: str
    city: str

    def load(self):
        return astuple(self)
