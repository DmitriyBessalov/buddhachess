from pydantic import BaseModel, EmailStr, validator


class User(BaseModel):
    username: str
    password: str


class UserRegister(User):
    email: EmailStr
    password2: str

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    class Config:
        orm_mode = True


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


def HTTPError(loc: str, msg: str):
    return {"detail": [{"loc": ["body", loc], "msg": msg}]}
