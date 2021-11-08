from random import randint
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.db import get_session
from app.shemas import auth as schemas_auth
from app.models import user as models_user
from app.services import auth as servises_auth

from app.routers.http_error import HTTP_Error

router = APIRouter()


# @router.post("/register")
# async def user_create(request: Request, user: schemas_auth.UserRegister, db=Depends(get_db)):
#     db_user = db.query(models_user.User).filter(models_user.User.username == user.username).first()
#     if user.username.find("@") != -1:
#         return HTTP_Error("username", "Username cannot contain '@'")
#     if db_user:
#         return HTTP_Error("username", "Username already in use")
#     db_user = db.query(models_user.User).filter(models_user.User.email == user.email).first()
#     if db_user:
#         return HTTP_Error("email", "Email already in use")
#
#     hashed_password = CryptContext(schemes='bcrypt', deprecated="auto").hash(user.password)
#
#     await servises_auth.create_user(db, user, hashed_password)
#
#     _user = schemas_auth.UserHashPassword(username=user.username, hashed_password=hashed_password, email=user.email)
#
#     await servises_auth.send_email("new_account", 'Подтвердите регистрацию на сайте "Шахматы Будды"', request, _user)
#
#     return await servises_auth.create_token(user.username, hashed_password)
#
#
# @router.post("/token")
# async def login(user: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
#     db_user = await servises_auth.get_user_from_username_or_email(user.username, db)
#     if db_user is None:
#         return HTTP_Error("username", "User not Found")
#     if CryptContext(schemes='bcrypt', deprecated="auto").verify(user.password, db_user.hashed_password):
#         return await servises_auth.create_token(db_user.username, db_user.hashed_password)
#     return HTTP_Error("password", "Wrong password")
#
#
# @router.get("/create_anonimous_token")
# async def create_anonimous_token(token: str = 'null'):
#     if token == "undefined" or token == "null":
#         return await servises_auth.create_token_anonimous('Anonimous_' + str(randint(1000000, 9999999)))
#     else:
#         return await servises_auth.get_current_user(token, True, db=Depends(get_db))
#
#
# @router.get("/me")
# async def user_info(user: schemas_auth.User = Depends(servises_auth.get_current_user)):
#     return user
#
#
# @router.patch("/password")
# async def password_update(password: schemas_auth.DoublePassword, user: schemas_auth.User = Depends(servises_auth.get_current_user), db=Depends(get_db)):
#     hashed_password = CryptContext(schemes='bcrypt', deprecated="auto").hash(password.password)
#
#     await servises_auth.update_password(db, user.username, hashed_password)
#
#     return await servises_auth.create_token(user.username, hashed_password)
#
#
# @router.patch("/verify_activation")
# async def verify_email(user: schemas_auth.User = Depends(servises_auth.get_current_user), db=Depends(get_db)):
#     return await servises_auth.verify__email(user.username, db)
#
#
# @router.post("/reset_password")
# async def reset_password(username: schemas_auth.ResetPassword, request: Request, db=Depends(get_db)):
#     db_user = await servises_auth.get_user_from_username_or_email(username.username, db)
#     if db_user is None:
#         return HTTP_Error("username", "User not Found")
#
#     response = await servises_auth.send_email("reset_password", 'Сброс пароля на сайте "Шахматы Будды"', request, db_user)
#
#     return {'send_mail': response}
