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

class requestdetails(BaseModel):
    email:str
    password:str
        
class TokenUsersSchema(BaseModel):
    access: str
    refresh: str

class changepassword(BaseModel):
    email:str
    old_password:str
    new_password:str

class resetpassword(BaseModel):
    email:str
    new_password:str

class ResetPasswordConfirm(BaseModel):
    code: str
    new_password: str