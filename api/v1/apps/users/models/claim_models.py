from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.orm import relationship, declarative_base
from api.v1.apps.users.models.association_tables import user_claims

Base = declarative_base()

class Claim(Base):
    __tablename__ = "claims"

    id = Column(BigInteger, primary_key=True)
    description = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    users = relationship("User", secondary=user_claims, back_populates="claims")