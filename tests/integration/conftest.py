import pytest
from sqlalchemy import delete
from app.users.user_profile.models import UserProfile


@pytest.fixture(autouse=True)
async def cleanup_user_profile(get_db_session):

    async with get_db_session as session:
        await session.execute(delete(UserProfile))
        await session.commit()
    yield
    