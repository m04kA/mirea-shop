from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, String, Table, ForeignKey

from .models import METADATA

metadata = METADATA

item = Table(
    "item",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("cost", String),
    Column("photo_path", String),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
)

ingredients = Table(
    "ingredient",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
)

ingredients_shawarma = Table(
    "ingredients_shawarma",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("ingredient_id", Integer, ForeignKey(ingredients.c.id)),
    Column("item_id", Integer, ForeignKey(item.c.id)),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
)
