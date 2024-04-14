from dataclasses import dataclass

@dataclass
class Image:
    link: str
    
    def load(self):
        return (
            self.link
        )
