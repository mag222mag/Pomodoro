import pytest
import pytest_asyncio
from app.settings import Settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.settings import Settings 
from app.infrastructure.database.database import Base


@pytest.fixture
def settings():
    return Settings()


engine = create_async_engine(url="postgresql+asyncpg://postgres:password@127.0.0.1:5432/pomodoro-test", future=True, echo=True, pool_pre_ping=True)


AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)

@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def get_db_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session
