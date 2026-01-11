from fastapi import APIRouter,FastAPI, status, HTTPException, Request, Depends
from core.logger_config import logger

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from database.session import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.factories.rest_api_factory  import RestAPIFactory
from api.v1.factories.factory import APIFactory
from api.v1.apps.users.services.users_services import UserCrudService
from api.v1.apps.users.schemas.user_schemas import UserCreate, UserRead, UserBase


router = APIRouter()
app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.state.limiter = limiter

factory: APIFactory = RestAPIFactory()

crud: UserCrudService = factory.crud("users")

@limiter.limit("10/minute")
@router.post('/create-users/', status_code=status.HTTP_201_CREATED)
async def create_users(request:Request, users: UserCreate, session: AsyncSession = Depends(get_async_session),):
    try: 

        users_data_create = users.dict() 
        return await crud.create(session=session, args=users_data_create)
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao cadastrar o usuário: {e}")

@limiter.limit("10/minute")
@router.get('/get-users/', status_code=status.HTTP_200_OK)
async def get_users(request:Request, session: AsyncSession = Depends(get_async_session),):
    try:

        return await crud.read(session=session)
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao listar o usuários: {e}")
   
@limiter.limit("10/minute")
@router.put('/update-users/{user_id}/', status_code=status.HTTP_200_OK)
async def update_users(request:Request, users_id: str, users: UserBase, session: AsyncSession = Depends(get_async_session),):
    try:

        users_data_update = users.dict(exclude_unset=True) 
        return await crud.update(session=session, users_id=users_id, **users_data_update)
    
    except HTTPException as http_exc:
            raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao atualizar usuário: {e}")
    
@limiter.limit("10/minute")
@router.delete('/delete-users/{user_id}/',status_code=status.HTTP_200_OK)
async def delete_role(request:Request, role_id: str, session: AsyncSession = Depends(get_async_session),):
    try:

        return await crud.delete(session=session, role_id=role_id)
    
    except HTTPException as http_exc:
            raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao deletar usuário: {e}")
    
    