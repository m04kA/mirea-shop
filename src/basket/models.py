from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship

from src.auth.models import User as user_model
from src.items.models import Item as item_model
from src.database import Base, metadata

order_item = Table(
    "order_item",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("item_id", Integer, ForeignKey("item.id")),
    Column("order_id", Integer, ForeignKey("order.id")),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
)

class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    orderNr = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship(
       "Item",
       secondary=order_item,
       back_populates="items",
       lazy="selectin"
    )

