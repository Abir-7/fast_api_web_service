from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)

# async_sessionmaker is the modern way to create async sessions in SQLAlchemy 2.0
SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,   # avoids lazy-load errors after commit
)

async def get_db():            # must be async
    async with SessionLocal() as session:
        yield session