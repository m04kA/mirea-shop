from typing import Optional, List

from pydantic import BaseModel


# from src.items.ingredients.schemas import Ingredient


class TypeItem(BaseModel):
    id: int
    name: str


class ItemBase(BaseModel):
    name: str
    price: float
    description: str
    item_type: TypeItem
    photo_path: Optional[str] = None
    available: Optional[bool] = True


class Item(ItemBase):
    id: int

    # created_at: Optional[str] = None
    # updated_at: Optional[str] = None

    class Config:
        orm_mode = True


class IngredientBase(BaseModel):
    name: str
    description: Optional[str]


class IngredientCreate(IngredientBase):
    pass


class Ingredient(IngredientBase):
    id: int

    # created_at: Optional[datetime] = None
    # updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ItemCreate(ItemBase):
    ingredients: List[Ingredient]


class ItemSchema(Item):
    ingredients: List[Ingredient]
