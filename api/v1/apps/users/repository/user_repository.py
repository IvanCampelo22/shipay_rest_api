from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api.v1.apps.users.models.user_models import User
from sqlalchemy import update

class UserRepository:
    def __init__(self, session):
        self.session = session

    async def create(self, user: User):
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_id(self, user_id: int):
        result = await self.session.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.role), selectinload(User.claims))
        )
        return result.scalar_one_or_none()

    async def list(self):
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.role), selectinload(User.claims))
        )
        return result.scalars().all()
    
    async def update(self, user_id: int, data: dict):
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(**data)
        )
        await self.session.commit()

        return await self.get_by_id(user_id)

    async def delete(self, user: User):
        await self.session.delete(user)
        await self.session.commit()