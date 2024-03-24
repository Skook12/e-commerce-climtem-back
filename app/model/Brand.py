from dataclasses import dataclass

@dataclass
class Brand:
    name: str
    
    def load(self):
        return (
            self.name
        )
