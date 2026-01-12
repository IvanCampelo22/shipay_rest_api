from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api.v1.apps.users.models.user_models import User
from sqlalchemy import update, insert
from api.v1.apps.users.models.association_tables import user_claims
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import extract, or_, case
import re
from api.v1.apps.users.models.role_models import Role
from api.v1.apps.users.models.claim_models import Claim
from api.v1.apps.users.search.user_search_interpreter import SearchInterpreter


# TODO add session in __init__ method
class UserRepository:
    def __init__(self):
        self._search = SearchInterpreter()

    async def add_claim(self, session, user_id: int, claim_id: int):
        await session.execute(
            insert(user_claims).values(user_id=user_id, claim_id=claim_id)
        )
        await session.commit()

    async def create(self, session, data: dict) -> User:
        user = User(**data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_by_id(self, session, user_id: int):
        result = await session.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.role), selectinload(User.claims))
        )
        return result.scalar_one_or_none()

    async def list(self, session):
        result = await session.execute(
            select(User)
            .options(selectinload(User.role), selectinload(User.claims))
        )
        return result.scalars().all()
    
    async def update(self, session, user_id: int, data: dict):
        await session.execute(
            update(User)
            .where(User.id == user_id)
            .values(**data)
        )
        await session.commit()

        return await self.get_by_id(session=session, user_id=user_id)

    async def delete(self, session, user: User):
        await session.delete(user)
        await session.commit()

    async def generic_filter_for_user(self, session: AsyncSession, **kwargs):
        filters = []

        search: str = kwargs.get("search")

        if search:
            search = search.strip().lower()

            m = re.fullmatch(r"(\d{1,2})/(\d{1,2})", search)
            if m:
                day = int(m.group(1))
                month = int(m.group(2))

                if 1 <= day <= 31 and 1 <= month <= 12:
                    filters.append(extract("day", User.created_at) == day)
                    filters.append(extract("month", User.created_at) == month)
                    return filters

            stype = self._search.detect_bool(search)

            if stype == self._search.SearchTypes.TRUE:
                filters.append(User.is_active.is_(True))
                return filters

            if stype == self._search.SearchTypes.FALSE:
                filters.append(User.is_active.is_(False))
                return filters

            date_info = self._search.detect_created_at_range(search)

            if date_info:
                if date_info["type"] == "year":
                    filters.append(extract("year", User.created_at) == date_info["year"])
                    return filters

                if date_info["type"] == "day":
                    filters.append(extract("day", User.created_at) == date_info["day"])
                    return filters

                if date_info["type"] == "day_or_month":
                    v = date_info["value"]
                    filters.append(
                        or_(
                            extract("month", User.created_at) == v,
                            extract("day", User.created_at) == v,
                        )
                    )
                    return filters

                if date_info["type"] == "range":
                    filters.append(User.created_at >= date_info["start"])
                    filters.append(User.created_at <= date_info["end"])
                    return filters

            filters.append(
                or_(
                    User.name.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                    User.role.any(
                        Role.description.ilike(f"%{search}%")
                    ),
                )
            )
            return filters

        params = {
            "user_name": lambda v: User.name.ilike(f"%{v}%"),
            "user_id": lambda v: User.id == v,
            "email": lambda v: User.email == v,
            "role_id": lambda v: User.role_id.any(
                Role.id.in_(v if isinstance(v, list) else [v])
            )
        }

        for key, func in params.items():
            value = kwargs.get(key)
            if value is not None:
                f = func(value)
                if f is not None:
                    filters.append(f)

        return filters
    
    async def mapping_order_users_by(self, order_by: str) -> Any:

        order_by_status = case(
            (User.is_active == True, 1),
            (User.is_active == False, 2),
            else_=0
        )

        return {
            "order_by_name": User.name.asc(),
            "order_by_status": order_by_status.asc(),
            "order_by_email": User.email.asc(),
            "order_by_created_at": User.created_at.asc(),
        }.get(order_by, User.name.asc())