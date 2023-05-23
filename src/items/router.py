from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import parse_obj_as

from src.database import get_async_session
from src.items.models import Item, Ingredient, item_ingredient, TypeItem
from src.items.schemas import IngredientCreate, ItemCreate, TypeItemCreate, ItemBase
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


@router.get("/all", response_model=List[item_schema])
async def get_all_type_items(session: AsyncSession = Depends(get_async_session)):
    query = select(Item)
    result = await session.execute(query)
    items = result.scalars().all()
    item_details = []
    for item in items:
        query_ingredients = select(Ingredient).join(item_ingredient).where(item_ingredient.c.item_id == item.id)
        ingredients = await session.execute(query_ingredients)
        ingredients = ingredients.scalars().all()
        ingredient_summaries = []
        for ing in ingredients:
            description = ing.description if ing.description else None
            ingredient_summaries.append(Ingredient(id=ing.id, name=ing.name, description=description))
        item_details.append(item_schema(
            id=item.id,
            name=item.name,
            price=item.price,
            description=item.description,
            item_type=item.item_type,
            photo_path=item.photo_path,
            available=item.available,
            ingredients=ingredient_summaries
        ))
    return item_details

@router.delete("/{item_id}/")
async def delete_one_ingredient(item_id: int, session: AsyncSession = Depends(get_async_session)):
    item = await session.get(Item, item_id)
    await session.delete(item)
    await session.commit()
    return {"status": "success"}

@router.put('/{item_id}/', response_model=item_schema)
async def update_ingredient(item_id: int, new_operation: ItemCreate, session: AsyncSession = Depends(get_async_session)):
    db_item = await session.get(Item, item_id)

    if new_operation.name:
        db_item.name = new_operation.name
    if new_operation.price:
        db_item.price = new_operation.price
    if new_operation.description:
        db_item.item_type = new_operation.item_type
    if new_operation.photo_path:
        db_item.photo_path = new_operation.photo_path
    if new_operation.available:
        db_item.available = new_operation.available
#
#     # TODO fix upgrade ingredients
#     # query = select(item_ingredient).where(item_ingredient.c.itme_id == item_id)
#     # result_ingredients_ids = await session.execute(query)
#     # old_ingredients_ids = result_ingredients_ids.scalars().all()
#     #
#     # for ingredient_id in new_operation.ingredients:
#     #     ingredient = await session.get(Ingredient, ingredient_id)
#     #     if ingredient:
#     #         db_item.ingredients
#
    await session.commit()
    await session.refresh(db_item)

    return db_item

# --------

# ---- type-items ----

@router_type_items.get("/{type_items_id}/", response_model=type_item_schema)
async def get_one_type_items(type_items_id: int, session: AsyncSession = Depends(get_async_session)):
    return await session.get(TypeItem, type_items_id)


@router_type_items.get("/all", response_model=List[type_item_schema])
async def get_all_type_items(session: AsyncSession = Depends(get_async_session)):
    query = select(TypeItem)
    result = await session.execute(query)
    return result.scalars().all()


@router_type_items.post("/")
async def add_one_type_items(new_operation: TypeItemCreate, session: AsyncSession = Depends(get_async_session)):
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

@router_ingredients.put('/{ingredient_id}/', response_model=IngredientCreate)
async def update_ingredient(ingredient_id: int, new_operation: IngredientCreate, session: AsyncSession = Depends(get_async_session)):
    db_ingredient = await session.get(Ingredient, ingredient_id)

    db_ingredient.name = new_operation.name

    await session.commit()
    await session.refresh(db_ingredient)

    return db_ingredient

# --------

# router.include_router(router_type_items)
# router.include_router(router_ingredients)
