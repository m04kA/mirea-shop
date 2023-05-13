from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship

from src.database import Base, metadata

item_ingredient = Table(
    "item_ingredient",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("item_id", Integer, ForeignKey("item.id")),
    Column("ingredient_id", Integer, ForeignKey("ingredient.id")),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
)

type_item = Table(
    "type_item",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
)


class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String)
    item_type = Column(ForeignKey(type_item.c.id))
    photo_path = Column(String)
    available = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    ingredients = relationship(
        "Ingredient",
        secondary=item_ingredient,
        back_populates="items",
        lazy="selectin"
    )


class Ingredient(Base):
    __tablename__ = "ingredient"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship(
        "Item",
        secondary=item_ingredient,
        back_populates="ingredients"
    )

