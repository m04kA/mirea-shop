# from datetime import datetime
# from typing import Optional
#
# from pydantic import BaseModel
#
#
# class IngredientBase(BaseModel):
#     name: str
#     description: Optional[str]
#
#
# class IngredientCreate(IngredientBase):
#     pass
#
#
# class Ingredient(IngredientBase):
#     id: int
#     # created_at: Optional[datetime] = None
#     # updated_at: Optional[datetime] = None
#
#     class Config:
#         orm_mode = True
