from sqlalchemy import Column, Integer, BigInteger, String, Date, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from api.v1.apps.users.models.association_tables import user_claims

from database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String(100), nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    created_at = Column(Date, nullable=False, server_default=func.current_date())
    updated_at = Column(Date, onupdate=func.current_date())
    is_active = Column(Boolean, default=True)

    role = relationship("Role", back_populates="users")
    claims = relationship("Claim", secondary=user_claims, back_populates="users")

class TokenTableUsers(Base):
    __tablename__ = "TokenTableUsers"
    user_id = Column(Integer)
    access_toke = Column(String(450), primary_key=True)
    refresh_toke = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.now)
