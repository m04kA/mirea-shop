from typing import Optional, List

from pydantic import BaseModel


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


class TypeItemBase(BaseModel):
    name: str


class TypeItem(TypeItemBase):
    id: int

    class Config:
        orm_mode = True


class TypeItemCreate(TypeItemBase):
    pass


class ItemBase(BaseModel):
    name: str
    price: float
    description: str
    item_type: int
    photo_path: Optional[str] = None
    available: Optional[bool] = True


class Item(ItemBase):
    id: int
    ingredients: List[Ingredient]

    # created_at: Optional[str] = None
    # updated_at: Optional[str] = None

    class Config:
        orm_mode = True


class ItemCreate(ItemBase):
    ingredients: List[int]


class ItemsSchema(Item):
    ingredients: List[Ingredient]
