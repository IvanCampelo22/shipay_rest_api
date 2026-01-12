from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Dict, Optional

from api.v1.apps.users.repository.user_repository import UserRepository
from api.v1.factories.interfaces.crud_interface import CrudInterface
from api.v1.apps.users.schemas.user_schemas import UserRead
from api.v1.apps.users.models.user_models import User
from api.v1.apps.users.models.claim_models import Claim
from api.v1.helpers.utils import generate_random_password
from api.v1.apps.users.auth.auth_handle import get_hashed_password
from core.logger_config import logger

MAX_BCRYPT_LEN = 72


class UserCrudService(CrudInterface):

    def __init__(self):
        self.repository = UserRepository()

    async def attach_claim(self, session, user_id: int, claim_id: int):
        user = await session.get(User, user_id)
        claim = await session.get(Claim, claim_id)

        if not user or not claim:
            raise HTTPException(status_code=404, detail="User or Claim not found")

        await self.repository.add_claim(session, user_id, claim_id)

    async def create(self, session, args: Dict[str, any]) -> Dict[str, str]:
        password = args.get("password")

        if not password:
            generated = generate_random_password(args["email"])
            raw_password = generated[:MAX_BCRYPT_LEN]
        else:
            raw_password = password[:MAX_BCRYPT_LEN]

        hashed = get_hashed_password(raw_password)
        args["password"] = hashed

        new_user = await self.repository.create(session=session, data=args)
        logger.success("Novo usuário criado com sucesso")

        return {"id": str(new_user.id)}

    async def read(self, session) -> List[UserRead]:
        role = await self.repository.list(session=session)
        if not role:
            logger.info("Nenhum usuário encontrado.")

        return role
    
    async def update(self, session, users_id: int, data: dict):
        user = await self.repository.get_by_id(session=session, user_id=users_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="usuário não encontrado."
            )

        await self.repository.update(
            session=session,
            user_id=users_id,
            data=data
        )

        return {"message": f"usuário {users_id}: atualizado com sucesso"}
    

    async def delete(self, session, users_id: str) -> Dict[str, str]:
        users_object = await self.repository.get_by_id(
            session=session,
            user_id=int(users_id)
        )

        if users_object is None:
            raise HTTPException(status_code=404, detail="usuário não encontrado.")

        await self.repository.delete(session=session, user=users_object)

        return {"message": f"usuário {users_object.name}: deletado com sucesso"}
        
    