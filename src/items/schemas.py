from typing import Optional, List

from pydantic import BaseModel
from src.items.ingredients.schemas import Ingredient


class TypeItem(BaseModel):
    id: int
    name: str


class ItemBase(BaseModel):
    name: str
    price: float
    description: str
    item_type: TypeItem
    available: bool
    photo_path: Optional[str] = None
    available: Optional[bool] = True


class ItemCreate(ItemBase):
    ingredient_ids: List[int] = []


class Item(ItemBase):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    ingredients_ids: List[Ingredient.id] = []

    class Config:
        orm_mode = True
