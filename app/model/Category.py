from dataclasses import dataclass, field

@dataclass
class Category:
    name: str
    
    def load(self):
        return (
            f'{self.name}'
        )
