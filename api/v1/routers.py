from fastapi.routing import APIRouter
from api.v1.controllers import users_controllers, claim_controllers, role_controllers

api_router = APIRouter()

api_router.include_router(users_controllers.router, prefix='/users', tags=['users'])
api_router.include_router(claim_controllers.router, prefix='/claim', tags=['claim'])
api_router.include_router(role_controllers.router, prefix='/role', tags=['role'])