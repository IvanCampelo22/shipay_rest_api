from fastapi import APIRouter,FastAPI, status, HTTPException, Request, Depends, Query
from core.logger_config import logger

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from database.session import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from api.v1.apps.users.schemas.user_schemas import UserCreate, UserUpdate, changepassword, TokenUsersSchema, requestdetails
from api.v1.apps.users.services.authentication import UsersAuthenticationService
from api.v1.apps.users.services.filters_services import UserFilterService
from api.v1.apps.users.services.users_services import UserCrudService
from api.v1.factories.rest_api_factory  import RestAPIFactory
from api.v1.apps.users.auth.auth_utils import JWTBearer
from api.v1.factories.factory import APIFactory


router = APIRouter()
app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.state.limiter = limiter

factory: APIFactory = RestAPIFactory()

crud: UserCrudService = factory.crud("users")
authentication: UsersAuthenticationService = factory.authentication("authentication")
filters: UserFilterService = factory.filters("filters_users")

@router.post('/logout', status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def logout(request: Request, credentials=Depends(JWTBearer()), session: AsyncSession = Depends(get_async_session), _=Depends(JWTBearer())):
    try:

        user_object = await authentication.logout(args=credentials, session=session)
        return user_object
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno ao fazer logout {e}.")

@router.post('/login', response_model=TokenUsersSchema, status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def login(request: Request, schema: requestdetails, session: AsyncSession = Depends(get_async_session)):
    try:

        user_object = await authentication.login(schema=schema, session=session)
        return user_object
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao fazer login: {e}")

@router.post('/change-password', status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("10/minute")
async def change_password(request: Request, request_change_password: changepassword, _=Depends(JWTBearer()), session: AsyncSession = Depends(get_async_session)):
    try: 
        
        user_object = await authentication.change_password(schema=request_change_password, session=session)
        return user_object
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno ao mudar senha do usuário.")

@router.post("/users/{user_id}/claims/{claim_id}")
async def assign_claim(user_id: int, claim_id: int, session: AsyncSession = Depends(get_async_session), _=Depends(JWTBearer())):
    try: 

        await crud.attach_claim(session, user_id, claim_id)
        return {"message": "Claim assigned successfully"}

    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno ao mudar senha do usuário.")

@limiter.limit("10/minute")
@router.post('/create-users/', status_code=status.HTTP_201_CREATED)
async def create_users(request:Request, users: UserCreate, session: AsyncSession = Depends(get_async_session)):
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
async def get_users(request:Request, session: AsyncSession = Depends(get_async_session), _=Depends(JWTBearer())):
    try:

        return await crud.read(session=session)
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao listar o usuários: {e}")
   
@router.get("/get-one-user", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def get_one_user(request: Request, users_id: int = None, _=Depends(JWTBearer()), session: AsyncSession = Depends(get_async_session)):
    try: 
        user_object = await filters.filter_by_id(args=users_id, session=session)
        return user_object

    except HTTPException as http_exc:
            raise http_exc
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")


@router.get("/filter", response_model=dict, status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def filter_users_endpoint(
    request: Request,
    _=Depends(JWTBearer()),
    is_active: Optional[bool] = Query(None),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    user_name: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    email: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    role_id: Optional[int] = Query(None),
    order_by: Optional[str] = Query(default="order_by_name"),
    session: AsyncSession = Depends(get_async_session),
):
    try:

        filters_kwargs = {
            "user_name": user_name,
            "user_id": user_id,
            "role_id": role_id,
            "is_active": is_active,
            "email": email,
            "search": search,
            "order_by": order_by
        }
        filters_kwargs = {k: v for k, v in filters_kwargs.items() if v is not None}

        result = await filters.filters(
            offset=offset,
            limit=limit,
            session=session,
            **filters_kwargs
        )

        return result

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao filtrar usuários: {e}"
        )

@limiter.limit("10/minute")
@router.put('/update-users/{user_id}/', status_code=status.HTTP_200_OK)
async def update_users(request:Request, users_id: int, users: UserUpdate, session: AsyncSession = Depends(get_async_session), _=Depends(JWTBearer())):
    try:

        users_data_update = users.dict(exclude_unset=True) 
        return await crud.update(session=session, users_id=users_id, data=users_data_update)
    
    except HTTPException as http_exc:
            raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao atualizar usuário: {e}")
    
@limiter.limit("10/minute")
@router.delete('/delete-users/{user_id}/',status_code=status.HTTP_200_OK)
async def delete_users(request:Request, user_id: str, session: AsyncSession = Depends(get_async_session), _=Depends(JWTBearer())):
    try:

        return await crud.delete(session=session, users_id=user_id)
    
    except HTTPException as http_exc:
            raise http_exc
    
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro interno ao deletar usuário: {e}")
    
    