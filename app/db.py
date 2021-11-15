from app.settings import settings
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
import databases

metadata = sqlalchemy.MetaData()
database = databases.Database(settings.DATABASE_URL)
engine = sqlalchemy.create_engine(settings.DATABASE_URL, echo=settings.DEBUG, connect_args={"check_same_thread": False})

Base = declarative_base()
