import enum
from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, String, Table, ForeignKey, MetaData

metadata = MetaData()


ingredient = Table(
    "ingredient",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
)