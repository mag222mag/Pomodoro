from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from app.users.user_profile.models import UserProfile
from app.users.user_profile.schema import UserCreateSchema


@dataclass
class UserRepository:
    db_session: AsyncSession

    async def get_user_by_email(self, email: str) -> UserProfile | None:
        async with self.db_session as session:
            result = await session.execute(select(UserProfile).where(UserProfile.email == email))
            return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreateSchema) -> UserProfile:
        query = insert(UserProfile).values(user_data.dict(exclude_none=True)).returning(UserProfile.id)
        async with self.db_session as session:
            user_id: int = (await session.execute(query)).scalar()
            await session.commit()
            await session.flush()
            return await self.get_user(user_id)

    async def get_user(self, user_id: int) -> UserProfile | None:
        async with self.db_session as session:
            result = await session.execute(select(UserProfile).where(UserProfile.id == user_id))
            return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> UserProfile | None:
        async with self.db_session as session:
            result = await session.execute(select(UserProfile).where(UserProfile.username == username))
            return result.scalar_one_or_none()