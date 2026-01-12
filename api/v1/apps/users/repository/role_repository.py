from sqlalchemy.future import select
from api.v1.apps.users.models.role_models import Role
from sqlalchemy import update


# TODO add session in __init__ method
class RoleRepository:

    async def create(self, session, data: dict) -> Role:
        user = Role(**data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_by_id(self, session, role_id: int):
        result = await session.execute(select(Role).where(Role.id == role_id))
        return result.scalar_one_or_none()

    async def list(self, session):
        result = await session.execute(select(Role))
        return result.scalars().all()
    
    async def update(self, session, role_id: int, data: dict):
        await session.execute(
            update(Role)
            .where(Role.id == role_id)
            .values(**data)
        )
        await session.commit()

        return await self.get_by_id(session=session, role_id=role_id)

    async def delete(self, session, role: Role):
        await session.delete(role)
        await session.commit()