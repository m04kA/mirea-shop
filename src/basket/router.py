from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import parse_obj_as

from src.database import get_async_session
from src.basket.models import Item, User, Order
from src.basket.schemas import ItemCreate, OrderCreate, OrderBase, Ingredient
from src.basket.schemas import User as user_schema
from src.basket.schemas import Item as item_schema
from src.basket.schemas import Order as order_schema
from src.items.models import item_ingredient

router = APIRouter(
    prefix="/orders",
    tags=["Oorders"]
)

router_item = APIRouter(
    prefix="/items",
    tags=["Items"]
)

router_users = APIRouter(
    prefix="/users",
    tags=["Users"]
)
# ---- ORDER ----

@router.post('/', response_model=order_schema)
async def create_order(new_operation: OrderCreate, session: AsyncSession = Depends(get_async_session)):

    order_dict = new_operation.dict()
    items_ids = order_dict.pop('item')
    users_ids = order_dict.pop('user')
    db_order = Order(**order_dict)
    for user_id in users_ids:
        user = await session.get(User, user_id)
        for item_id in items_ids:
            item = await session.get(Item, item_id)
            if item:
                db_order.ingredients.append(item)
        if user:
            db_order.ingredients.append(user)
    session.add(db_order)
    await session.commit()
    await session.refresh(db_order)

    return db_order


@router.get("/{order_id}/")
async def get_one_order(order_id: int, session: AsyncSession = Depends(get_async_session)):
    return await session.get(Order, order_id)


@router.get("/all", response_model=List[order_schema])
async def get_all_type_orders(session: AsyncSession = Depends(get_async_session)):
    query = select(Order)
    result = await session.execute(query)
    orders = result.scalars().all()
    order_details = []
    for order in orders:
        query_items = select(Item).join(Order).where(Order.c.order_id == Item.id)
        query_users = select(User).join(Order).where(Order.c.order_id == User.id)
        items = await session.execute(query_items)
        users = await session.execute(query_users)
        items = items.scalars().all()
        users = users.scalars().all()
        item_summaries = []
        user_summaries = []
        for elem in items:
            description = elem.description if elem.description else None
            photo_path = elem.photo_path if elem.photo_path else None
            available = elem.available if elem.available else None
            item_summaries.append(Item(id=elem.id, name=elem.name, price = elem.price, description=description, item_type = elem.item_type, photo_path=photo_path, available=available))
        for user in users:
            email = user.email if user.email else None
            user_summaries.append(User(id=user.id, username=user.username, email = email))
        order_details.append(order_schema(
            items=item_summaries,
            orders=user_summaries
        ))
    return order_details

@router.delete("/{order_id}/")
async def delete_one_ingredient(order_id: int, session: AsyncSession = Depends(get_async_session)):
    order = await session.get(Order, order_id)
    await session.delete(order)
    await session.commit()
    return {"status": "success"}

@router.put('/{order_id}/', response_model=order_schema)
async def update_ingredient(order_id: int, item_id: int, new_operation: OrderCreate, session: AsyncSession = Depends(get_async_session)):
    db_order = await session.get(Order, order_id)

#    query = select(Order).where(Order.c.order_id == order_id)
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