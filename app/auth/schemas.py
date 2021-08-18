from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class UserWithEmail(User):
    email: EmailStr


class UserHashPassword(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr

    class Config:
        orm_mode = True


class ResetPassword(BaseModel):
    username: str


class TokenData(BaseModel):
    username: str
    permissions: str = "user"
