from sqlalchemy import TIMESTAMP, Column, Integer, String, Table

from src.database import metadata

order = Table(
    "order",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("quantity", String),
    Column("type", String),
    Column("dateOrdered", TIMESTAMP),
    Column("dateOfDelivery", TIMESTAMP)
)