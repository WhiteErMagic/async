import datetime
import os

from sqlalchemy import Integer, String, JSON
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from atexit import register

POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '1234')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'flask_db')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')


PG_DSN = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_async_engine(PG_DSN)
SessionDB = async_sessionmaker(bind=engine)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Сharacter(Base):
    __tablename__ = 'character'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    json: Mapped[dict] = mapped_column(JSON)
    # birth_year: Mapped[str] = mapped_column(String(50), nullable=True)
    # eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    # films: Mapped[str] = mapped_column(String(1000), nullable=True)
    # gender: Mapped[str] = mapped_column(String(50), nullable=True)
    # hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    # height: Mapped[str] = mapped_column(String(50), nullable=True)
    # homeworld: Mapped[str] = mapped_column(String(50), nullable=True)
    # mass: Mapped[str] = mapped_column(String(50), nullable=True)
    # name: Mapped[str] = mapped_column(String(50), nullable=True)
    # skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    # species: Mapped[str] = mapped_column(String(1000), nullable=True)
    # starships: Mapped[str] = mapped_column(String(1000), nullable=True)
    # vehicles: Mapped[str] = mapped_column(String(1000), nullable=True)
    # created: Mapped[str] = mapped_column(String(50), nullable=True)
    # edited: Mapped[str] = mapped_column(String(50), nullable=True)
    # url: Mapped[str] = mapped_column(String(50), nullable=True)


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)