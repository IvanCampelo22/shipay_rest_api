from pydantic import BaseModel

class ClaimBase(BaseModel):
    description: str
    active: bool = True

class ClaimCreate(ClaimBase):
    pass

class ClaimRead(ClaimBase):
    id: int

    class Config:
        orm_mode = True