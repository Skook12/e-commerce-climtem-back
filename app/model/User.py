from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    password: str
    phone: int

    def load(self):
        return (
            f'{self.name}',
            f'{self.email}',
            f'{self.password}',
            self.phone
        )
