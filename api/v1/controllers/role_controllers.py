from fastapi import APIRouter,FastAPI, status, HTTPException, Request, Depends
from core.logger_config import logger

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from database.session import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.apps.users.schemas.role_schemas import RoleCreate, RoleBase
from api.v1.apps.users.services.role_services import RoleCrudService
from api.v1.factories.rest_api_factory  import RestAPIFactory
from api.v1.apps.users.auth.auth_utils import JWTBearer
from api.v1.factories.factory import APIFactory

router = APIRouter()
app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.state.limiter = limiter

factory: APIFactory = RestAPIFactory()

crud: RoleCrudService = factory.crud("role")

@limiter.limit("10/minute")
@router.post('/create-role/', status_code=status.HTTP_201_CREATED)
async def create_role(request:Request, claim: RoleCreate, session: AsyncSession = Depends(get_async_session), _=Depends(JWTBearer())):
    try: 

        role_data_create = claim.dict() 
        return await crud.create(session=session, args=role_data_create)
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao cadastrar o perfil de acesso: {e}")

@limiter.limit("10/minute")
@router.get('/get-role/', status_code=status.HTTP_200_OK)
async def get_role(request:Request, session: AsyncSession = Depends(get_async_session), _=Depends(JWTBearer())):
    try:

        return await crud.read(session=session)
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao listar o perfis de acesso: {e}")
   
@limiter.limit("10/minute")
@router.put('/update-role/{role_id}/', status_code=status.HTTP_200_OK)
async def update_role(request:Request, role_id: str, role: RoleBase, session: AsyncSession = Depends(get_async_session), _=Depends(JWTBearer())):
    try:

        role_data_update = role.dict(exclude_unset=True) 
        return await crud.update(session=session, role_id=role_id, **role_data_update)
    
    except HTTPException as http_exc:
            raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao atualizar perfil de acesso: {e}")
    
@limiter.limit("10/minute")
@router.delete('/delete-role/{role_id}/',status_code=status.HTTP_200_OK)
async def delete_role(request:Request, role_id: str, session: AsyncSession = Depends(get_async_session), _=Depends(JWTBearer())):
    try:

        return await crud.delete(session=session, role_id=role_id)
    
    except HTTPException as http_exc:
            raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao deletar perfil de acesso: {e}")
    
    