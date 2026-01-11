from datetime import date
from typing import List, Optional
from .role_schemas import RoleRead
from .claim_schemas import ClaimRead
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role_id: int

class UserRead(UserBase):
    id: int
    created_at: date
    updated_at: Optional[date]

    role: RoleRead
    claims: List[ClaimRead] = []

    class Config:
        orm_mode = True