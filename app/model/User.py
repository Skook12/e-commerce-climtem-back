from dataclasses import dataclass, astuple

@dataclass
class User:
    name: str
    email: str
    password: str
    cpf: str
    phone: int

    def load(self):
        return astuple(self)
