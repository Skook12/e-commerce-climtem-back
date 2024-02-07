from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Address:
    id: int = field(init=False)
    user_id: int
    number: int
    complement: Optional[str]
    cep: str
    city: int
