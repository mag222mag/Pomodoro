from sqlalchemy import create_engine                     # <-- НОВЫЙ ИМПОРТ
from sqlalchemy.orm import sessionmaker, DeclarativeBase, declared_attr  # <-- ДОБАВИЛИ sessionmaker
from typing import Any
from settings import Settings

# --- НОВЫЙ БЛОК: ПОДКЛЮЧЕНИЕ К БД ---
settings = Settings()
engine = create_engine(settings.db_url)
Session = sessionmaker(engine)
# --- КОНЕЦ НОВОГО БЛОКА ---


class Base(DeclarativeBase):
    id: Any
    __name__: str
    __allow_unmapped__ = True
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


# --- НОВАЯ ФУНКЦИЯ ---
def get_db_session():
    return Session()
# --- КОНЕЦ НОВОЙ ФУНКЦИИ ---