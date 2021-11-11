from random import randint
from fastapi import APIRouter, Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from starlette.responses import RedirectResponse
from app.shemas import auth as schemas_auth
from app.services import auth as servises_auth
from app.services.http_error import HTTP_Error
from app.models.user import User
from app.db import database

router = APIRouter()


@router.on_event("startup")
async def startup() -> None:
    if not database.is_connected:
        await database.connect()


@router.on_event("shutdown")
async def shutdown() -> None:
    if database.is_connected:
        await database.disconnect()


@router.post("/register")
async def user_create(request: Request, user: schemas_auth.UserRegister):
    if user.username.find("@") != -1:
        return HTTP_Error("username", "Username cannot contain '@'")

    db_user = await User.objects.get_or_none(username=user.username)
    if db_user is not None:
        return HTTP_Error("username", "Username already in use")

    db_user = await User.objects.get_or_none(email=user.email)
    if db_user is not None:
        return HTTP_Error("email", "Email already in use")

    hashed_password = CryptContext(schemes='bcrypt', deprecated="auto").hash(user.password)

    await User.objects.create(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )

    await servises_auth.send_email(
        "new_account",
        'Подтвердите регистрацию на сайте "Шахматы Будды"',
        request,
        user.username,
        user.email,
        hashed_password
    )

    return await servises_auth.create_token(user.username, hashed_password)


@router.post("/token")
async def login(response: Response, user: OAuth2PasswordRequestForm = Depends()):
    db_user = await servises_auth.get_user_from_username_or_email(user.username)
    if db_user is None:
        return HTTP_Error("username", "User not Found")
    if CryptContext(schemes='bcrypt', deprecated="auto").verify(user.password, db_user.hashed_password):
        res = await servises_auth.create_token(db_user.username, db_user.hashed_password)
        response.set_cookie(key="Authorization", value=f"Bearer {res['access_token']}", max_age=604800, httponly=True)
        return res
    return HTTP_Error("password", "Wrong password")


@router.get("/create_or_get_anonimous_token")
async def create_or_get_anonimous_token(token: str = 'null'):
    if token == "undefined" or token == "null":
        return await servises_auth.create_token_anonimous('Anonimous_' + str(randint(1000000, 9999999)))
    else:
        return await servises_auth.get_current_user(token, True)


@router.get("/me")
async def user_info(user: schemas_auth.User = Depends(servises_auth.get_current_user)):
    return user


@router.patch("/password")
async def password_update(response: Response, password: schemas_auth.DoublePassword, user: schemas_auth.User = Depends(servises_auth.get_current_user)):
    hashed_password = CryptContext(schemes='bcrypt', deprecated="auto").hash(password.password)

    db_user = User.objects.update(username=user.username, hashed_password=hashed_password).one()

    auth = await servises_auth.create_token(db_user.username, db_user.hashed_password)
    res = RedirectResponse("/", status_code=302)
    response.set_cookie(key="Authorization", value=f"Bearer {auth['access_token']}", max_age=604800, httponly=True)
    return res


@router.patch("/verify_activation")
async def verify_email(user: schemas_auth.User = Depends(servises_auth.get_current_user)):
    db_user = User.objects.update(username=user.username, is_verified=True).one()
    user.is_verified = True
    return jsonable_encoder(db_user)


@router.post("/reset_password")
async def reset_password(username: schemas_auth.ResetPassword, request: Request):
    db_user = await servises_auth.get_user_from_username_or_email(username.username)
    if db_user is None:
        return HTTP_Error("username", "User not Found")

    response = await servises_auth.send_email(
        "reset_password",
        'Сброс пароля на сайте "Шахматы Будды"',
        request,
        db_user.username,
        db_user.email,
        db_user.hashed_password
    )

    return {'send_mail': response}
