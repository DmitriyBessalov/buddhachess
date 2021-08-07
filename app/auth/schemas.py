from pydantic import BaseModel
import typing


class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    username: str = None


class UserOut(UserBase):
    pass


class UserCreate(UserBase):
    password: str
    email: str
    is_active: bool = True
    username: str = None

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    password: typing.Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"
