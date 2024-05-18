from dataclasses import dataclass, astuple

@dataclass
class User:
    name: str
    email: str
    password: str
    cpf: str
    phone: int
    adm: bool = False

    def load(self):
        return astuple(self)
