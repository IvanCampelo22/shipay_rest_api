from pydantic import BaseModel

class RoleBase(BaseModel):
    description: str

class RoleCreate(RoleBase):
    pass

class RoleRead(RoleBase):
    id: int

    class Config:
        orm_mode = True