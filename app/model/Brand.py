from dataclasses import dataclass, field

@dataclass
class Brand:
    name: str

    def load(self):
        return (
            f'{self.name}'
        )
