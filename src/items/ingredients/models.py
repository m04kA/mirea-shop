# import enum
# from datetime import datetime
#
# from sqlalchemy import TIMESTAMP, Column, Integer, String, Table, ForeignKey, MetaData
# from sqlalchemy.orm import relationship
#
# from src.database import Base, metadata
# from src.items.models import item_ingredient
#
#
#
# # ingredient = Table(
# #     "ingredient",
# #     metadata,
# #     Column("id", Integer, primary_key=True),
# #     Column("name", String, nullable=False),
# #     Column("description", String),
# #     Column("created_at", TIMESTAMP, default=datetime.utcnow),
# #     Column("updated_at", TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
# # )
# class Ingredient(Base):
#     __tablename__ = "ingredient"
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     description = Column(String)
#     created_at = Column(TIMESTAMP, default=datetime.utcnow)
#     updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
#
#     items = relationship(
#         "Item",
#         secondary=item_ingredient,
#         back_populates="ingredients",
#         lazy="subquery"
#     )