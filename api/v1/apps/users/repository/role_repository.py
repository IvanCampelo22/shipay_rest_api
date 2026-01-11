from sqlalchemy.future import select
from api.v1.apps.users.models.role_models import Role
from sqlalchemy import update

class RoleRepository:
    def __init__(self, session):
        self.session = session

    async def create(self, role: Role):
        self.session.add(role)
        await self.session.commit()
        await self.session.refresh(role)
        return role

    async def get_by_id(self, role_id: int):
        result = await self.session.execute(select(Role).where(Role.id == role_id))
        return result.scalar_one_or_none()

    async def list(self):
        result = await self.session.execute(select(Role))
        return result.scalars().all()
    
    async def update(self, role_id: int, data: dict):
        await self.session.execute(
            update(Role)
            .where(Role.id == role_id)
            .values(**data)
        )
        await self.session.commit()

        return await self.get_by_id(role_id)

    async def delete(self, role: Role):
        await self.session.delete(role)
        await self.session.commit()