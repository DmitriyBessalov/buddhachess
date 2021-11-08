from pydantic import BaseModel, EmailStr, validator


class User(BaseModel):
    username: str
    password: str


class DoublePassword(BaseModel):
    password: str
    password2: str

    @validator('password2')
    def passwords_match(cls, v, values):
        if v != values['password']:
            raise ValueError('Passwords do not match')
        return v


class UserRegister(DoublePassword):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserHashPassword(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

    class Config:
        orm_mode = True


class ResetPassword(BaseModel):
    username: str
