from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.items.models import item, ingredient, ingredient_shawarma

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)
