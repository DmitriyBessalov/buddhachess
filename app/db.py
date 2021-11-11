from app.settings import settings
import sqlalchemy
import databases

metadata = sqlalchemy.MetaData()
database = databases.Database(settings.DATABASE_URL)
engine = sqlalchemy.create_engine(settings.DATABASE_URL, echo=settings.DEBUG)
