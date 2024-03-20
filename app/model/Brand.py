from dataclasses import dataclass, field

@dataclass
class Brand:
    product_id: int = field(init=False)
    name: str

    def load(self):
        return (
            self.product_id,
            f'{self.name}'
        )
