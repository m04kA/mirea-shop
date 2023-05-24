from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship

from src.auth.models import role
from src.database import Base, metadata

Order = Table(
    "item_ingredient",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("item_id", Integer, ForeignKey("item.id")),
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("order_id", Integer, nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
)

class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String)
    item_type = Column(ForeignKey("type_item.id"))
    photo_path = Column(String)
    available = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    ingredients = relationship(
        "Ingredient",
        secondary=order,
        back_populates="items",
        lazy="selectin"
    )

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    role_id = Column(Integer, ForeignKey(role.c.id))
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    items = relationship(
        "Item",
        secondary=order,
        back_populates="ingredients"
    )
