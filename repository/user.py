from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from models import UserProfile
from schema.user import UserCreateSchema

@dataclass
class UserRepository:
    db_session: AsyncSession

    async def get_user_by_email(self, email: str) -> UserProfile | None:
        async with self.db_session as session:
            result = await session.execute(select(UserProfile).where(UserProfile.email == email))
            return result.scalar_one_or_none()

    async def create_user(self, user: UserCreateSchema) -> UserProfile:
        query = insert(UserProfile).values(**user.model_dump()).returning(UserProfile.id)
        async with self.db_session as session:
            user_id = await session.execute(query)
            await session.commit()
            # после вставки получаем пользователя
            return await self.get_user(user_id.scalar())

    async def get_user(self, user_id: int) -> UserProfile | None:
        async with self.db_session as session:
            result = await session.execute(select(UserProfile).where(UserProfile.id == user_id))
            return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> UserProfile | None:
        async with self.db_session as session:
            result = await session.execute(select(UserProfile).where(UserProfile.username == username))
            return result.scalar_one_or_none()
        