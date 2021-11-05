from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String


class User(SQLModel, table=True):
    username: str = Field(primary_key=True, nullable=False)
    email: EmailStr = Field(sa_column=Column("email", String, unique=True))
    hashed_password: str
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    group: str = Field(default='gamer')

    # date_birthday = Column(DateTime)
    # phone = models.IntegerField(verbose_name="Телефон", blank=True, null=True)
    # telegram = Column(String, unique=True)
    # ava = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Аватар", blank=True, null=True)
