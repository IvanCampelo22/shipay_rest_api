from sqlalchemy.future import select
from sqlalchemy import update
from api.v1.apps.users.models.claim_models import Claim

class ClaimRepository:
    def __init__(self, session):
        self.session = session

    async def create(self, claim: Claim):
        self.session.add(claim)
        await self.session.commit()
        await self.session.refresh(claim)
        return claim

    async def get_by_id(self, claim_id: int):
        result = await self.session.execute(
            select(Claim).where(Claim.id == claim_id)
        )
        return result.scalar_one_or_none()

    async def list(self):
        result = await self.session.execute(select(Claim))
        return result.scalars().all()
    
    async def update(self, claim_id: int, data: dict):
        await self.session.execute(
            update(Claim)
            .where(Claim.id == claim_id)
            .values(**data)
        )
        await self.session.commit()

        return await self.get_by_id(claim_id)

    async def delete(self, claim: Claim):
        await self.session.delete(claim)
        await self.session.commit()