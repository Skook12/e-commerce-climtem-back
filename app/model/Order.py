from dataclasses import dataclass, astuple
from datetime import datetime

@dataclass
class Order:
    user_id: int
    buy_date: datetime
    status: str
    payment_type: str
    expiration: datetime
    total_bought: float
    
    def load(self):
        return astuple(self)

@dataclass
class ShoppingCar:
    order_id: int
    product_id: int
    quantity: int
    
    def load(self):
        return astuple(self)