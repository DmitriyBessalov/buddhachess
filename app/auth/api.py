from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.auth.servises import get_user_from_username_or_email, \
    create_user, \
    get_current_user, \
    create_token, \
    update_password, \
    send_email,\
    verify__email

from db import get_db
from app.auth import schemas
from app.auth import models


router = APIRouter()


@router.post("/register")
async def user_create(user: schemas.UserRegister, request: Request, db=Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if user.username.find("@") != -1:
        raise HTTPException(status_code=404, detail=schemas.HTTPError("username", "Username cannot contain '@'"))
    if db_user:
        raise HTTPException(status_code=404, detail=schemas.HTTPError("username", "Username already in use"))
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=404, detail=schemas.HTTPError("email", "Email already in use"))

    hashed_password = CryptContext(schemes='bcrypt', deprecated="auto").hash(user.password)

    await create_user(db, user, hashed_password)

    _user = schemas.UserHashPassword(username=user.username, hashed_password=hashed_password, email=user.email)

    await send_email("new_account", 'Подтвердите регистрацию на сайте "Шахматы Будды"', request, _user)

    return await create_token(user.username, hashed_password)


@router.post("/token")
async def login(user: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    db_user = await get_user_from_username_or_email(user.username, db)
    if db_user is None:
        return HTTPException(status_code=404, detail="User not Found")

    if CryptContext(schemes='bcrypt', deprecated="auto").verify(user.password, db_user.hashed_password):
        return await create_token(db_user.username, db_user.hashed_password)
    return HTTPException(status_code=404, detail="Wrong password")


@router.get("/me")
async def user_info(user: schemas.User = Depends(get_current_user)):
    return user


@router.patch("/password")
async def password_update(password: str, user: schemas.User = Depends(get_current_user), db=Depends(get_db)):
    hashed_password = CryptContext(schemes='bcrypt', deprecated="auto").hash(password)

    await update_password(db, user.username, hashed_password)

    return await create_token(user.username, hashed_password)


@router.patch("/verify_activation")
async def verify_email(user: schemas.User = Depends(get_current_user), db=Depends(get_db)):
    return await verify__email(user.username, db)


@router.post("/reset_password")
async def reset_password(username: schemas.ResetPassword, request: Request, db=Depends(get_db)):
    db_user = await get_user_from_username_or_email(username.username, db)
    if db_user is None:
        return HTTPException(status_code=404, detail="User not Found")

    response = await send_email("reset_password", 'Сброс пароля на сайте "Шахматы Будды"', request, db_user)

    return HTMLResponse(response)
