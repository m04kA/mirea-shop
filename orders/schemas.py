from datetime import datetime

from pydantic import BaseModel

class OrderCreate(BaseModel):
    id: int
    quantity: str
    type: str
    dateOrdered: datetime
    dateOfDelivery: datetime