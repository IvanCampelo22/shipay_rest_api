from fastapi import APIRouter,FastAPI, status, HTTPException, Request, Depends
from core.logger_config import logger

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from database.session import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.factories.rest_api_factory  import RestAPIFactory
from api.v1.factories.factory import APIFactory
from api.v1.apps.users.services.claim_services import ClaimCrudService
from api.v1.apps.users.schemas.claim_schemas import ClaimCreate, ClaimRead, ClaimBase


router = APIRouter()
app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.state.limiter = limiter

factory: APIFactory = RestAPIFactory()

crud: ClaimCrudService = factory.crud("claim")

@limiter.limit("10/minute")
@router.post('/create-claim/', status_code=status.HTTP_201_CREATED)
async def create_claim(request: Request, claim: ClaimCreate, session: AsyncSession = Depends(get_async_session),):
    try: 

        claim_data_create = claim.dict() 
        return await crud.create(session=session, args=claim_data_create)
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao cadastrar o declaração: {e}")
    
@limiter.limit("10/minute")
@router.get('/get-claim/', status_code=status.HTTP_200_OK)
async def get_claim(request: Request, session: AsyncSession = Depends(get_async_session),):
    try:

        return await crud.read(session=session)
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao listar o declaração: {e}")
   
@limiter.limit("10/minute")
@router.put('/update-claim/{claim_id}/', status_code=status.HTTP_200_OK)
async def update_claim(request:Request, claim_id: str, claim: ClaimBase, session: AsyncSession = Depends(get_async_session),):
    try:

        claim_data_update = claim.dict(exclude_unset=True) 
        return await crud.update(session=session, claim_id=claim_id, **claim_data_update)
    
    except HTTPException as http_exc:
            raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao atualizar declaração: {e}")
    
@limiter.limit("10/minute")
@router.delete('/delete-claim/{claim_id}/',status_code=status.HTTP_200_OK)
async def delete_claim(request:Request, claim_id: str, session: AsyncSession = Depends(get_async_session),):
    try:

        return await crud.delete(session=session, claim_id=claim_id)
    
    except HTTPException as http_exc:
            raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao deletar declaração: {e}")
    
    