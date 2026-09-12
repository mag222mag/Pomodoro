from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.tasks.models import Tasks, Categories
from app.tasks.schema import TaskCreateSchema

class TaskRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_tasks(self):
        async with self.db_session as session:
            result = await session.execute(select(Tasks))
            return result.scalars().all()

    async def get_task(self, task_id: int) -> Tasks | None:
        async with self.db_session as session:
            result = await session.execute(select(Tasks).where(Tasks.id == task_id))
            return result.scalar_one_or_none()

    async def get_user_tasks(self, task_id: int, user_id: int) -> Tasks | None:
        async with self.db_session as session:
            result = await session.execute(
                select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
            )
            return result.scalar_one_or_none()

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        task_model = Tasks(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
            user_id=user_id
        )
        async with self.db_session as session:
            session.add(task_model)
            await session.commit()
            await session.refresh(task_model)
            return task_model.id

    async def delete_task(self, task_id: int, user_id: int) -> None:
        query = delete(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()

    async def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name == category_name)
        async with self.db_session as session:
            result = await session.execute(query)
            return result.scalars().all()

    async def update_task_name(self, task_id: int, name: str) -> Tasks:
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        async with self.db_session as session:
            task_id_result = await session.execute(query)
            await session.commit()
            # возвращаем обновлённую задачу
            return await self.get_task(task_id)