from dataclasses import dataclass
from typing import Optional

@dataclass
class Address:
    user_id: int
    number: int
    complement: Optional[str]
    cep: str
    city: str

    def load(self):
        return (
            self.user_id,
            self.number,
            f'{self.complement}',
            f'{self.cep}',
            f'{self.city}'
        )

