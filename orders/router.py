from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

router = APIRouter(
    prefix="/orders",
    tags=["Order"]
)

@router.get("")
async def get_specific_orders(
        operation_type: str,
        session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(order).where(order.c.type == operation_type)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.all(),
            "details": None
        }
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("")
async def add_specific_operations(new_order: OrderCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(order).values(**new_order.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/main")
async def main(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(1))
    return result.all()