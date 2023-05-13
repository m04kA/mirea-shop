from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.items.models import Item, Ingredient, item_ingredient
from src.items.schemas import Item, IngredientCreate

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

# @router.get("/{item_id}/")
# async def get_one_item(item_id: int, session: AsyncSession = Depends(get_async_session)):
#     query = select(item).where(item.c.id == item_id)
#     result = await session.execute(query)
#     return result.all()
#
# @router.get("/all", response_model=List[Item])
# async def get_all_items(session: AsyncSession = Depends(get_async_session)):
#     query = select(item)
#     result = await session.execute(query)
#     return result.all()

@router.get("/ingredients/{ingredient_id}/")
async def get_one_ingredient(ingredient_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Ingredient).where(Ingredient.id == ingredient_id)
    result = await session.execute(query)
    return result.all()

@router.get("/ingredients/all", response_model=List[Ingredient])
async def get_all_ingredients(session: AsyncSession = Depends(get_async_session)):
    query = select(Ingredient)
    result = await session.execute(query)
    return result.all()


@router.post("/ingredients/")
async def add_one_ingredient(new_operation: IngredientCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Ingredient).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/ingredients/{ingredient_id}/")
async def delete_one_ingredient(ingredient_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(Ingredient).where(Ingredient.c.id == ingredient_id)
    await session.execute(query)
    await session.commit()
    return {"status": "success"}

