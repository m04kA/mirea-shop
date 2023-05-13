from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.items.models import Item, Ingredient, item_ingredient, TypeItem
from src.items.schemas import IngredientCreate, ItemCreate, TypeItemCreate
from src.items.schemas import TypeItem as type_item_schema
from src.items.schemas import Ingredient as ingredient_schema
from src.items.schemas import Item as item_schema

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

router_type_items = APIRouter(
    prefix="/type-items",
    tags=["Type items"]
)

router_ingredients = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"]
)
# ---- ITEM ----

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


@router.get("/{item_id}/")
async def get_one_item(item_id: int, session: AsyncSession = Depends(get_async_session)):
    return await session.get(Item, item_id)

# --------

# ---- type-items ----

@router_type_items.get("/{type_items_id}/", response_model=type_item_schema)
async def get_one_type_items(type_items_id: int, session: AsyncSession = Depends(get_async_session)):
    return await session.get(TypeItem, type_items_id)
    # query = select(type_item).where(type_item.c.id == type_items_id)
    # result = await session.execute(query)
    # return result.all()[0]


@router_type_items.get("/all", response_model=List[type_item_schema])
async def get_all_type_items(session: AsyncSession = Depends(get_async_session)):
    query = select(TypeItem)
    result = await session.execute(query)
    return result.scalars().all()


@router_type_items.post("/")
async def add_one_type_items(new_operation: TypeItemCreate, session: AsyncSession = Depends(get_async_session)):
    # stmt = insert(type_item).values(**new_operation.dict())
    # await session.execute(stmt)
    # await session.commit()
    db_type_item = TypeItem(**new_operation.dict())
    session.add(db_type_item)
    await session.commit()
    await session.refresh(db_type_item)
    return {"status": "success"}


@router_type_items.delete("/{type_items_id}/")
async def delete_one_type_items(type_items_id: int, session: AsyncSession = Depends(get_async_session)):
    type_item = await session.get(TypeItem, type_items_id)
    await session.delete(type_item)
    await session.commit()
    return {"status": "success"}

@router_type_items.put('/{type_items_id}/', response_model=type_item_schema)
async def update_type_items(type_items_id: int, new_operation: TypeItemCreate, session: AsyncSession = Depends(get_async_session)):
    # query = select(type_item).where(type_item.c.id == type_items_id)
    # result = await session.execute(query)
    db_type_item = await session.get(TypeItem, type_items_id)

    db_type_item.name = new_operation.name

    await session.commit()
    await session.refresh(db_type_item)

    return db_type_item

# --------


# ---- ingredients ----

@router_ingredients.get("/{ingredient_id}/")
async def get_one_ingredient(ingredient_id: int, session: AsyncSession = Depends(get_async_session)):
    return await session.get(Ingredient, ingredient_id)


@router_ingredients.get("/all", response_model=List[ingredient_schema])
async def get_all_ingredients(session: AsyncSession = Depends(get_async_session)):
    query = select(Ingredient)
    result = await session.execute(query)
    return result.scalars().all()


@router_ingredients.post("/")
async def add_one_ingredient(new_operation: IngredientCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Ingredient).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router_ingredients.delete("/{ingredient_id}/")
async def delete_one_ingredient(ingredient_id: int, session: AsyncSession = Depends(get_async_session)):
    ingredient = await session.get(Ingredient, ingredient_id)
    await session.delete(ingredient)
    await session.commit()
    return {"status": "success"}

# --------

router.include_router(router_type_items)
router.include_router(router_ingredients)
