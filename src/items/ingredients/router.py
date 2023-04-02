from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .models import ingredient
from .schemas import IngredientCreate

router = APIRouter(
    prefix="/items/ingredients",
    tags=["Ingredients"]
)


@router.get("/{ingredient_id}/")
async def get_one_ingredient(ingredient_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(ingredient).where(ingredient.c.id == ingredient_id)
    result = await session.execute(query)
    return result.all()

# TODO It`s not working(((
# @router.get("/")
# async def get_all_ingredients(session: AsyncSession = Depends(get_async_session)):
#     query = select(ingredient)
#     result = await session.execute(query)
#     return result.fetchall()


@router.post("/")
async def add_one_ingredient(new_operation: IngredientCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(ingredient).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/{ingredient_id}/")
async def delete_one_ingredient(ingredient_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(ingredient).where(ingredient.c.id == ingredient_id)
    await session.execute(query)
    await session.commit()
    return {"status": "success"}
