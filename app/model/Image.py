from dataclasses import dataclass, astuple

@dataclass
class Image:
    product_id:int
    path: str
    
    def load(self):
        return astuple(self)
