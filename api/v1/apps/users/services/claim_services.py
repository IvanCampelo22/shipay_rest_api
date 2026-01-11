from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Dict, Optional

from api.v1.apps.users.repository.claim_repository import ClaimRepository
from api.v1.factories.interfaces.crud_interface import CrudInterface
from api.v1.apps.users.schemas.claim_schemas import ClaimRead

from database.session import async_session
from core.logger_config import logger


class ClaimCrudService(CrudInterface):

    def __init__(self):
        self.repository = ClaimRepository(session=AsyncSession)

    @async_session
    async def create(self, args: Dict[str, any]) -> Dict[str, str]:
        new_claim = await self.repository.create(args=args)
        logger.success("Nova declaração registrada com sucesso")
        return {"id": str(new_claim.id)}

    @async_session
    async def read(self) -> List[ClaimRead]:
        claim = await self.repository.list()
        if not claim:
            logger.info("Nenhum declaração encontrada.")

        return claim
    
    @async_session 
    async def update(self, claim_id: int, data: Dict[str, Optional[str]]) -> Dict[str, str]:
        claim_data = await self.repository.get_by_id(claim_id)
        if not claim_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="declaração não encontrada."
            )

        for key, value in data.items():
            if value is not None and hasattr(claim_data, key):
                setattr(claim_data, key, value)

        await self.repository.update(claim_id=claim_id, data=claim_data)
        return {"message": f"declaração {claim_data.id}: atualizada com sucesso"}
    

    @async_session
    async def delete(self, claim_id: int) -> Dict[str, str]:
        claim_object = await self.repository.get_by_id(claim_id==claim_id)

        if claim_object is None:
            raise HTTPException(status_code=404, detail="declaração não encontrada.")

        await self.repository.delete(claim=claim_id)
        return {"message": f"declaração {claim_object.description}: deletada com sucesso"}
        
    