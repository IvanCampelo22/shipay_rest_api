from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Dict, Optional

from api.v1.apps.users.repository.role_repository import RoleRepository
from api.v1.factories.interfaces.crud_interface import CrudInterface
from api.v1.apps.users.schemas.role_schemas import RoleRead

from core.logger_config import logger


class RoleCrudService(CrudInterface):

    def __init__(self):
        self.repository = RoleRepository()

    async def create(self, session, args: Dict[str, any]) -> Dict[str, str]:
        new_role = await self.repository.create(session=session, data=args)
        logger.success("Novo perfil de acesso criado com sucesso")
        return {"id": str(new_role.id)}

    async def read(self, session) -> List[RoleRead]:
        role = await self.repository.list(session=session)
        if not role:
            logger.info("Nenhum perfil de acesso encontrado.")

        return role
    
    async def update(self, session, role_id: int, data: Dict[str, Optional[str]]) -> Dict[str, str]:
        role_data = await self.repository.get_by_id(session=session, role_id=role_id)
        if not role_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="perfil de acesso não encontrado."
            )

        for key, value in data.items():
            if value is not None and hasattr(role_data, key):
                setattr(role_data, key, value)

        await self.repository.update(session=session, role_id=role_id, data=role_data)
        return {"message": f"perfil de acesso {role_data.id}: atualizado com sucesso"}
    

    async def delete(self, session, role_id: int) -> Dict[str, str]:
        role_object = await self.repository.get_by_id(session=session, role_id=role_id)

        if role_object is None:
            raise HTTPException(status_code=404, detail="perfil de acesso não encontrado.")

        await self.repository.delete(role=role_id)
        return {"message": f"perfil de acesso {role_object.description}: deletado com sucesso"}
        
    