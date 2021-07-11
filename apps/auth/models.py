from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Column, String, Integer, DateTime, Boolean, CHAR
from db import Base
import uuid


class User(Base, SQLAlchemyBaseUserTable):
    id = Column(CHAR(length=36), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True)
    date_birthday = Column(DateTime)
    # phone = models.IntegerField(verbose_name="Телефон", blank=True, null=True)
    telegram = Column(String, unique=True)
    # ava = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Аватар", blank=True, null=True)

users = User.__table__