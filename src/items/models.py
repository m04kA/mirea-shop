import enum
from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, Table, ForeignKey, MetaData, Enum

from src.items.ingredients.models import ingredient

metadata = MetaData()


type_item = Table(
    "type_item",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
)

item = Table(
    "item",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("price", Integer, nullable=False),
    Column("description", String),
    Column("item_type", ForeignKey(type_item.c.id)),
    Column("photo_path", String),
    Column("available", Boolean, default=True),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
)

ingredient_shawarma = Table(
    "item_ingredient",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("ingredient_id", Integer, ForeignKey(ingredient.c.id)),
    Column("item_id", Integer, ForeignKey(item.c.id)),
)
