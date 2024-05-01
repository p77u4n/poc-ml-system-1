from dino_seedwork_be import get_env
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_posgres_uri() -> str:
    host = get_env("DB_HOST", "localhost")
    port = get_env("DB_PORT", 5432)
    password = get_env("DB_PASSWORD")
    user = get_env("DB_USER")
    db_name = get_env("DB_NAME")
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_async_engine(get_posgres_uri(), connect_args={})
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)
