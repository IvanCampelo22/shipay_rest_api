from sqlalchemy.future import select
from sqlalchemy import update
from api.v1.apps.users.models.claim_models import Claim


# TODO add session in __init__ method
class ClaimRepository:

    async def create(self, session, data: dict) -> Claim:
        claim = Claim(**data)
        session.add(claim)
        await session.commit()
        await session.refresh(claim)
        return claim

    async def get_by_id(self, session, claim_id: int):
        result = await session.execute(
            select(Claim).where(Claim.id == claim_id)
        )
        return result.scalar_one_or_none()

    async def list(self, session):
        result = await session.execute(select(Claim))
        return result.scalars().all()
    
    async def update(self, session, claim_id: int, data: dict):
        await session.execute(
            update(Claim)
            .where(Claim.id == claim_id)
            .values(**data)
        )
        await session.commit()

        return await self.get_by_id(claim_id)

    async def delete(self, session, claim: Claim):
        await session.delete(claim)
        await session.commit()