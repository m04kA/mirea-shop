from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.items.models import Item, Ingredient, item_ingredient, type_item
from src.items.schemas import IngredientCreate, ItemCreate, TypeItem, TypeItemCreate
from src.items.schemas import Ingredient as ingredient_schema
from src.items.schemas import Item as item_schema

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


@router.post('/', response_model=item_schema)
async def create_item(new_operation: ItemCreate, session: AsyncSession = Depends(get_async_session)):

    item_dict = new_operation.dict()
    ingredients_ids = item_dict.pop('ingredients')
    db_item = Item(**item_dict)
    for ingredient_id in ingredients_ids:
        ingredient = await session.get(Ingredient, ingredient_id)
        if ingredient:
            db_item.ingredients.append(ingredient)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)

    return db_item
    # stmt = insert(Ingredient).values(**item_dict)
    # test = await session.execute(stmt)
    # await session.commit()


    # for ingredient_id in ingredients_ids:
    #     ingredient = await session.get(Ingredient, ingredient_id)
    #     if ingredient:
    #         stmt = insert(item_ingredient).values(**{'item_id': })
    #         await session.execute(stmt)
    #     if db_ingredient is None:
    #         return Response('Ingredient does not exist', 500)
    #
    #     item_object.ingredients.append(db_ingredient[0])
    #
    # session.add(item_object)
    # await session.commit()
    # await session.refresh(item_object)
    #
    # return item_object

@router.get("/{item_id}/")
async def get_one_item(item_id: int, session: AsyncSession = Depends(get_async_session)):
    return await session.get(Item, item_id)


@router.get("/type-items/{type_items_id}/")
async def get_one_type_items(type_items_id: int, session: AsyncSession = Depends(get_async_session)):
    return await session.get(type_item, type_items_id)


@router.get("/type-items/all", response_model=List[TypeItem])
async def get_all_type_items(session: AsyncSession = Depends(get_async_session)):
    query = select(type_item)
    result = await session.execute(query)
    return result.all()


@router.post("/type-items/")
async def add_one_type_items(new_operation: TypeItemCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(type_item).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/type-items/{type_items_id}/")
async def delete_one_type_items(type_items_id: int, session: AsyncSession = Depends(get_async_session)):
    ingredient = await session.get(type_item, type_items_id)
    await session.delete(ingredient)
    await session.commit()
    return {"status": "success"}


@router.get("/ingredients/{ingredient_id}/")
async def get_one_ingredient(ingredient_id: int, session: AsyncSession = Depends(get_async_session)):
    return await session.get(Ingredient, ingredient_id)


@router.get("/ingredients/all", response_model=List[ingredient_schema])
async def get_all_ingredients(session: AsyncSession = Depends(get_async_session)):
    query = select(Ingredient)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/ingredients/")
async def add_one_ingredient(new_operation: IngredientCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Ingredient).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/ingredients/{ingredient_id}/")
async def delete_one_ingredient(ingredient_id: int, session: AsyncSession = Depends(get_async_session)):
    ingredient = await session.get(Ingredient, ingredient_id)
    await session.delete(ingredient)
    await session.commit()
    return {"status": "success"}
