from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from settings import Settings 

settings = Settings()

engine = create_async_engine(url=Settings().db_url, future=True, echo=True, pool_pre_ping=True)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)

async def get_db_session() -> AsyncSession: # type: ignore
    async with AsyncSessionFactory() as session:
        yield session