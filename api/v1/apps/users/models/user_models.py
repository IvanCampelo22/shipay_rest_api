from sqlalchemy import Column, Integer, BigInteger, String, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from api.v1.apps.users.models.association_tables import user_claims

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    created_at = Column(Date, nullable=False)
    updated_at = Column(Date)

    role = relationship("Role", back_populates="users")
    claims = relationship("Claim", secondary=user_claims, back_populates="users")