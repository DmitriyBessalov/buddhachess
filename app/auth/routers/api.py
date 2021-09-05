from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from db import get_db
from app.auth import schemas, models, servises
from app.base.schemas import HTTP_Error

router = APIRouter()


@router.post("/register")
async def user_create(request: Request, user: schemas.UserRegister, db=Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if user.username.find("@") != -1:
        return HTTP_Error("username", "Username cannot contain '@'")
    if db_user:
        return HTTP_Error("username", "Username already in use")
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        return HTTP_Error("email", "Email already in use")

    hashed_password = CryptContext(schemes='bcrypt', deprecated="auto").hash(user.password)

    await servises.create_user(db, user, hashed_password)

    _user = schemas.UserHashPassword(username=user.username, hashed_password=hashed_password, email=user.email)

    await servises.send_email("new_account", 'Подтвердите регистрацию на сайте "Шахматы Будды"', request, _user)

    return await servises.create_token(user.username, hashed_password)


@router.post("/token")
async def login(user: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    db_user = await servises.get_user_from_username_or_email(user.username, db)
    if db_user is None:
        return HTTP_Error("username", "User not Found")
    if CryptContext(schemes='bcrypt', deprecated="auto").verify(user.password, db_user.hashed_password):
        return await servises.create_token(db_user.username, db_user.hashed_password)
    return HTTP_Error("password", "Wrong password")


@router.get("/me")
async def user_info(user: schemas.User = Depends(servises.get_current_user)):
    return user


@router.patch("/password")
async def password_update(password: schemas.DoublePassword, user: schemas.User = Depends(servises.get_current_user), db=Depends(get_db)):
    hashed_password = CryptContext(schemes='bcrypt', deprecated="auto").hash(password.password)

    await servises.update_password(db, user.username, hashed_password)

    return await servises.create_token(user.username, hashed_password)


@router.patch("/verify_activation")
async def verify_email(user: schemas.User = Depends(servises.get_current_user), db=Depends(get_db)):
    return await servises.verify__email(user.username, db)


@router.post("/reset_password")
async def reset_password(username: schemas.ResetPassword, request: Request, db=Depends(get_db)):
    db_user = await servises.get_user_from_username_or_email(username.username, db)
    if db_user is None:
        return HTTP_Error("username", "User not Found")

    response = await servises.send_email("reset_password", 'Сброс пароля на сайте "Шахматы Будды"', request, db_user)

    return {'send_mail': response}
