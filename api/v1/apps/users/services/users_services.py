from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Dict, Optional

from api.v1.apps.users.repository.user_repository import UserRepository
from api.v1.factories.interfaces.crud_interface import CrudInterface
from api.v1.apps.users.schemas.user_schemas import UserRead

from database.session import async_session
from core.logger_config import logger


class UserCrudService(CrudInterface):

    def __init__(self):
        self.repository = UserRepository(session=AsyncSession)

    @async_session
    async def create(self, args: Dict[str, any]) -> Dict[str, str]:
        new_role = await self.repository.create(args=args)
        logger.success("Novo usuário criado com sucesso")
        return {"id": str(new_role.id)}

    @async_session
    async def read(self) -> List[UserRead]:
        role = await self.repository.list()
        if not role:
            logger.info("Nenhum usuário encontrado.")

        return role
    
    @async_session 
    async def update(self, role_id: int, data: Dict[str, Optional[str]]) -> Dict[str, str]:
        role_data = await self.repository.get_by_id(role_id)
        if not role_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="usuário não encontrado."
            )

        for key, value in data.items():
            if value is not None and hasattr(role_data, key):
                setattr(role_data, key, value)

        await self.repository.update(role_id=role_id, data=role_data)
        return {"message": f"usuário {role_data.id}: atualizado com sucesso"}
    

    @async_session
    async def delete(self, role_id: int) -> Dict[str, str]:
        role_object = await self.repository.get_by_id(role_id==role_id)

        if role_object is None:
            raise HTTPException(status_code=404, detail="usuário não encontrado.")

        await self.repository.delete(role=role_id)
        return {"message": f"usuário {role_object.description}: deletado com sucesso"}
        
    