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

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

class User(UserBase):
    id: int

    # created_at: Optional[str] = None
    # updated_at: Optional[str] = None

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass

class OrderBase(BaseModel):
    pass

class Order(OrderBase):
    id: int
    items: List[Ingredient]
    users: List[User]

    # created_at: Optional[str] = None
    # updated_at: Optional[str] = None

    class Config:
        orm_mode = True


class OrderCreate(ItemBase):
    items: List[int]
    users: List[int]

class OrderSchema(Item):
    items: List[Ingredient]
    users: List[User]