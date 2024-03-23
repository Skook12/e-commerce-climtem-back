from dataclasses import dataclass

@dataclass
class Category:
    name: str
    
    def load(self):
        return (
            self.name
        )
