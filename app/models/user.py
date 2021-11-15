from sqlalchemy import Column, String, Integer, Boolean
from app.db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    group = Column(String, default='gamer')
    # date_birthday = Column(DateTime)
    # telegram = Column(String, unique=True)
    # ava = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Аватар", blank=True, null=True)


user_table = User.__table__
