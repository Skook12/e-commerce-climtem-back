from dataclasses import dataclass, astuple

@dataclass
class User:
    name: str
    email: str
    password: str
    phone: int

    def load(self):
        return astuple(self)
