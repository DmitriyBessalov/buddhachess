from app.settings import settings
import sqlalchemy
import databases

# note lack of declarative_base
metadata = sqlalchemy.MetaData()
database = databases.Database(settings.DATABASE_URL)
engine = sqlalchemy.create_engine(settings.DATABASE_URL)


#
# engine = create_async_engine(DATABASE_URL, echo=True, future=True)
# Base = declarative_base()
#
# async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#
#
# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session
