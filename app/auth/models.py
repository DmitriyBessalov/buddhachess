from sqlalchemy import Column, String, Integer, DateTime, Boolean, CHAR
from db import Base


class User(Base):
    __tablename__ = "user"

    username = Column(String, primary_key=True, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    # date_birthday = Column(DateTime)
    # phone = models.IntegerField(verbose_name="Телефон", blank=True, null=True)
    # telegram = Column(String, unique=True)
    # ava = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Аватар", blank=True, null=True)


users = User.__table__