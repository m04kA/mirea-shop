from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import parse_obj_as

from src.basket.schemas import OrderCreate
from src.database import get_async_session
from src.basket.models import Order as order_model
from src.auth.models import User as user_model
from src.items.models import Item as item_model
from src.basket.schemas import Order as order_schema
router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# ---- ORDER ----

@router.post('/', response_model=order_schema)
async def create_order(new_operation: OrderCreate, session: AsyncSession = Depends(get_async_session)):

    order_dict = new_operation.dict()
    items_ids = order_dict.pop('item')
    db_order = order_model(**order_dict)
    for item_id in items_ids:
        item = await session.get(item_model, item_id)
        if item:
            db_order.ingredients.append(item)
    session.add(db_order)
    await session.commit()
    await session.refresh(db_order)

    return db_order


@router.get("/{order_id}/")
async def get_one_order(order_id: int, session: AsyncSession = Depends(get_async_session)):
    return await session.get(order_model, order_id)


@router.get("/all", response_model=List[order_schema])
async def get_all_type_orders(session: AsyncSession = Depends(get_async_session)):
    query = select(order_model)
    result = await session.execute(query)
    orders = result.scalars().all()
    return orders


@router.delete("/{order_id}/")
async def delete_one_ingredient(order_id: int, session: AsyncSession = Depends(get_async_session)):
    order = await session.get(order_model, order_id)
    await session.delete(order)
    await session.commit()
    return {"status": "success"}

@router.put('/{order_id}/', response_model=order_schema)
async def update_ingredient(order_id: int, item_id: int, new_operation: OrderCreate, session: AsyncSession = Depends(get_async_session)):
    db_order = await session.get(order_model, order_id)

#    query = select(order_model).where(order_model.c.order_id == order_id)
#    result_orders_ids = await session.execute(query)
#    old_ingredients_ids = result_orders_ids.scalars().all()
#
#    for ingredient_id in new_operation.ingredients:
#        ingredient = await session.get(Ingredient, ingredient_id)
#        if ingredient:
#              b_order.ingredients

    await session.commit()
    await session.refresh(db_order)

    return db_order