import ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# from core.config import settings

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# DATABASE_URL = (
#     f"postgresql+asyncpg://{settings.DB_USER}:"
#     f"{settings.DB_PASSWORD}"
#     f"@{settings.DB_HOST}:"
#     f"{settings.DB_PORT}/"
#     f"{settings.DB_NAME}"
# )

DATABASE_URL = (
    f"postgresql+asyncpg://postgres:"
    f"12345678"
    f"@localhost:"
    f"5432/"
    f"postgres"
)

print(DATABASE_URL)

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True,
    connect_args={
        "password": "12345678",
        "ssl": ssl_context,
    },
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base()

async def get_async_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

def async_session(func):
    async def wrapper(*args, **kwargs):
        async with AsyncSessionLocal() as session:
            try:
                result = await func(session, *args, **kwargs)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    return wrapper