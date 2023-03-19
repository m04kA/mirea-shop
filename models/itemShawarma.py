from sqlalchemy import TIMESTAMP, Column, Integer, String, Table, ForeignKey, Boolean

from src.database import metadata

item = Table(
    "item",
    metadata,
    Column("shawarma_id", Integer, primary_key=True),
    Column("name", String),
    Column("cost", String),
    Column("photo_path", String),
    Column("created_at", TIMESTAMP),
    Column("updated_at", TIMESTAMP)
)

ingredients = Table(
    "ingredients",
    metadata,
    Column("ingredients_id", Integer, primary_key=True),
    Column("name", String)
)

ingredients_shawarma = Table(
    "ingredients_shawarma",
    metadata,
    Column("ingredients_id", Integer, ForeignKey(ingredients.c.ingredients_id)),
    Column("shawarma_id", Integer, ForeignKey(item.c.shawarma_id)),
    Column("shaw_ingr_pkey", Integer, primary_key = True)
)