from api.v1.apps.users.schemas.user_schemas import UserRead, UserCreate, UserBase
from api.v1.factories.interfaces.filters_interface import FiltersInterface
from api.v1.apps.users.models.user_models import User
from api.v1.apps.users.repository.user_repository import UserRepository
from typing import Any

from sqlalchemy import select, func, and_, true
from sqlalchemy.orm import joinedload

from sqlalchemy.exc import SQLAlchemyError

class UserFilterService(FiltersInterface):

    def __init__(self):
        self.repository = UserRepository()
    
    async def filter_by_id(self, args, session):
        result = await session.execute(
            select(User)
            .options(
                joinedload(User.role),
                joinedload(User.claims),
            )
            .where(User.id == args)
        )
        user = result.unique().scalar_one_or_none()
        
        if not user:
            return None

        user_schema = UserRead.from_orm(user).dict()
        return user_schema
    
    # TODO how to create generic filter with those all joinedload?
    async def filters(self, offset, limit, session, **kwargs):
        try:
            filters = await self.repository.generic_filter_for_user(session=session, **kwargs)

            real_offset = offset * limit
            order_by_rule: Any = await self.repository.mapping_order_users_by(kwargs.get("order_by", "order_by_name"))

            query = (
                select(User)
                .where(and_(true(), *filters))
                .options(
                    joinedload(User.role),
                    joinedload(User.claims),
                )
                .order_by(order_by_rule)
                .limit(limit)
                .offset(real_offset)
            )

            result = await session.execute(query)
            users = result.unique().scalars().all()

            user_data = [
                UserRead.from_orm(user)
                for user in users
            ]

            count_query = select(func.count()).select_from(User).where(and_(true(), *filters))
            count_result = await session.execute(count_query)
            total = count_result.scalar()

            return {
                "users": user_data,
                "total": total
            }

        except Exception as e:
            raise Exception(f"Erro ao listar usuários: {str(e)}")

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error