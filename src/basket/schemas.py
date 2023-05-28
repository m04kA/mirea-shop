from typing import Optional, List

from pydantic import BaseModel
from src.auth.schemas import UserRead
from src.items.schemas import Item

class OrderBase(BaseModel):
    orderNr: str
class Order(OrderBase):
    id: int
    items: List[Item]
    user: UserRead

    # created_at: Optional[str] = None
    # updated_at: Optional[str] = None

    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    items: List[int]
    user_id: int