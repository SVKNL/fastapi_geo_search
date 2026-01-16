from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config.settings import Settings


settings = Settings()

engine = create_async_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=False, autocommit=False
)


async def get_db():
    async with SessionLocal() as db:
        yield db
