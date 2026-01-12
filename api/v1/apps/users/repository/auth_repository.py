from sqlalchemy.future import select
from typing import Any
from api.v1.apps.users.services.users_services import User

# TODO add session in __init__ method
class AuthRepository:

    async def validation_users_for_do_login(self, table_value, schema_value: Any, session: Any):
        query = await session.execute(select(User).where(table_value == schema_value))
        object = query.scalar()
        return object