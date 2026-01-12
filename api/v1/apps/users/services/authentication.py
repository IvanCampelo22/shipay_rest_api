import os, datetime

from jose import jwt
from fastapi import status
from sqlalchemy import select
from fastapi.exceptions import HTTPException

from api.v1.apps.users.repository.auth_repository import AuthRepository
from api.v1.factories.interfaces.auth_interface import AuthInterface
from api.v1.apps.users.auth.auth_handle import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
)
from api.v1.apps.users.models.user_models import User, TokenTableUsers


ALGORITHM=os.getenv("ALGORITHM")
JWT_SECRET_KEY=os.getenv("JWT_SECRET_ANALYTICS_KEY")
JWT_REFRESH_SECRET_KEY=os.getenv("JWT_REFRESH_SECRET_ANALYTICS_KEY")

class UsersAuthenticationService(AuthInterface):

    def __init__(self):
        self.repository = AuthRepository()

    async def login(self, schema, session):
        user_object = await self.repository.validation_users_for_do_login(User.email, schema.email, session)

        if user_object is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email incorreto")
        
        if not user_object.is_active: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Seu usuário está inativo.")
        
        hashed_password = user_object.password
        if not verify_password(schema.password, hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha incorreta"
            )
        
        access = create_access_token(
            user_object.id,
            user_object.email,
            user_object.role_id
        )
        refresh = create_refresh_token(user_object.id)

        token_db = TokenTableUsers(
            user_id=user_object.id,
            access_toke=access,
            refresh_toke=refresh,
            status=True
        )
        session.add(token_db)

        await session.commit()

        return {
            "access": access,
            "refresh": refresh,
        }
    
    async def logout(self, args: str, session):
        # HACK how to get better this try/catch? 
        try:
            payload = jwt.decode(args, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token inválido")

        user_id = payload['sub']

        threshold = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        result = await session.execute(
            select(TokenTableUsers).where(TokenTableUsers.created_date < threshold)
        )
        old_tokens = result.scalars().all()
        
        for token_entry in old_tokens:
            await session.delete(token_entry)

        await session.commit()

        result = await session.execute(
            select(TokenTableUsers).where(
                TokenTableUsers.user_id == int(user_id),
                TokenTableUsers.access_toke == str(args)
            )
        )
        existing_token = result.scalars().first()

        if existing_token:
            existing_token.status = False
            await session.commit()
            await session.refresh(existing_token)

        return {"message": "Logout realizado com sucesso"}

    async def change_password(self, schema, session):
        user = await self.repository.validation_users_for_do_login(User.email, schema_value=schema.email, session=session)
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

        if not verify_password(schema.old_password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Senha antiga inválida")
        
        encrypted_password = get_hashed_password(schema.new_password)
        user.password = encrypted_password
        await session.commit()
        
        return {"message": "Senha alterada com sucesso"}