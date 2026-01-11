from fastapi import APIRouter,FastAPI, status, HTTPException, Request
from core.logger_config import logger

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from api.v1.factories.rest_api_factory  import RestAPIFactory
from api.v1.factories.factory import APIFactory
from api.v1.apps.users.services.role_services import RoleCrudService
from api.v1.apps.users.schemas.role_schemas import RoleCreate, RoleRead, RoleBase


router = APIRouter()
app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.state.limiter = limiter

factory: APIFactory = RestAPIFactory()

crud: RoleCrudService = factory.crud("users")

@limiter.limit("10/minute")
@router.post('/create-users/', status_code=status.HTTP_201_CREATED)
async def create_users(claim: RoleCreate, request=Request):
    try: 

        role_data_create = claim.dict() 
        return await crud.create(args=role_data_create)
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao cadastrar o usuário: {e}")

@limiter.limit("10/minute")
@router.get('/get-users/', status_code=status.HTTP_200_OK)
async def get_users(request=Request):
    try:

        return await crud.read(RoleRead)
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao listar o usuários: {e}")
   
@limiter.limit("10/minute")
@router.put('/update-users/{user_id}/', status_code=status.HTTP_200_OK)
async def update_users(role_id: str, role: RoleBase, request=Request):
    try:

        role_data_update = role.dict(exclude_unset=True) 
        return await crud.update(role_id=role_id, **role_data_update)
    
    except HTTPException as http_exc:
            raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao atualizar usuário: {e}")
    
@limiter.limit("10/minute")
@router.delete('/delete-users/{user_id}/',status_code=status.HTTP_200_OK)
async def delete_role(role_id: str, request=Request):
    try:

        return await crud.delete(role_id=role_id)
    
    except HTTPException as http_exc:
            raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao deletar usuário: {e}")
    
    