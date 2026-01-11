from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Dict, Optional

from api.v1.apps.users.repository.user_repository import UserRepository
from api.v1.factories.interfaces.crud_interface import CrudInterface
from api.v1.apps.users.schemas.user_schemas import UserRead

from core.logger_config import logger


class UserCrudService(CrudInterface):

    def __init__(self):
        self.repository = UserRepository()

    async def create(self, session, args: Dict[str, any]) -> Dict[str, str]:
        new_role = await self.repository.create(session=session, args=args)
        logger.success("Novo usuário criado com sucesso")
        return {"id": str(new_role.id)}

    async def read(self, session) -> List[UserRead]:
        role = await self.repository.list(session=session)
        if not role:
            logger.info("Nenhum usuário encontrado.")

        return role
    
    async def update(self, session, users_id: int, data: Dict[str, Optional[str]]) -> Dict[str, str]:
        users_data = await self.repository.get_by_id(session=session, user_id=users_id)
        if not users_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="usuário não encontrado."
            )

        for key, value in data.items():
            if value is not None and hasattr(users_data, key):
                setattr(users_data, key, value)

        await self.repository.update(session=session, users_id=users_id, data=users_data)
        return {"message": f"usuário {users_data.id}: atualizado com sucesso"}
    

    async def delete(self, session, users_id: int) -> Dict[str, str]:
        users_object = await self.repository.get_by_id(session=session, users_id=users_id)

        if users_object is None:
            raise HTTPException(status_code=404, detail="usuário não encontrado.")

        await self.repository.delete(user=users_id)
        return {"message": f"usuário {users_object.description}: deletado com sucesso"}
        
    