from sqlalchemy import Table, Column, BigInteger, ForeignKey
from database.session import Base

user_claims = Table(
    "user_claims",
    Base.metadata,
    Column("user_id", BigInteger, ForeignKey("users.id"), primary_key=True),
    Column("claim_id", BigInteger, ForeignKey("claims.id"), primary_key=True),
)