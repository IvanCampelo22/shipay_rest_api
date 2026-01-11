from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api.v1.apps.users.models.user_models import User
from sqlalchemy import update


# TODO add session in __init__ method
class UserRepository:

    async def create(self, session, user: User):
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_by_id(self, session, user_id: int):
        result = await session.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.role), selectinload(User.claims))
        )
        return result.scalar_one_or_none()

    async def list(self, session):
        result = await session.execute(
            select(User)
            .options(selectinload(User.role), selectinload(User.claims))
        )
        return result.scalars().all()
    
    async def update(self, session, user_id: int, data: dict):
        await session.execute(
            update(User)
            .where(User.id == user_id)
            .values(**data)
        )
        await session.commit()

        return await self.get_by_id(session=session, user_id=user_id)

    async def delete(self, session, user: User):
        await session.delete(user)
        await session.commit()