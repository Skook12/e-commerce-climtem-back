from dataclasses import dataclass, astuple
from datetime import datetime
from .const import OrderStatus, PaymentType

@dataclass
class Order:
    user_id: int
    buy_date: datetime
    status: OrderStatus
    payment_type: PaymentType
    expiration: datetime
    total_bought: float
    track_id: str
    transport_name: str
    estimated_time: datetime
    freight_value: float
    
    def load(self):
        return astuple(self)

@dataclass
class ShoppingCar:
    order_id: int
    product_id: int
    quantity: int
    
    def load(self):
        return astuple(self)