import ormar
from pydantic import EmailStr
from app.db import database, metadata


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    email: EmailStr = ormar.String(unique=True, max_length=31)
    username: str = ormar.String(unique=True, max_length=31)
    password: str = ormar.String(pydantic_only=True, max_length=31)
    hashed_password: str = ormar.String(max_length=127)
    is_active: bool = ormar.Boolean(default=False)
    is_verified: bool = ormar.Boolean(default=False)
    group: str = ormar.String(default='gamer', max_length=7)

    # date_birthday = Column(DateTime)
    # phone = models.IntegerField(verbose_name="Телефон", blank=True, null=True)
    # telegram = Column(String, unique=True)
    # ava = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Аватар", blank=True, null=True)
