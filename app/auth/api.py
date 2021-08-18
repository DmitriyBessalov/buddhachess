from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
import emails
from emails.template import JinjaTemplate
from passlib.context import CryptContext

from app.auth.servises import get_user_from_username_or_email,\
    create_user,\
    get_current_user,\
    create_token,\
    update_password

from settings import settings
from db import get_db
from app.auth import schemas
from app.auth import models

from pathlib import Path

router = APIRouter()


@router.post("/register")
async def user_create(user: schemas.UserWithEmail, db=Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if user.username.find("@") != -1:
        raise HTTPException(status_code=404, detail="Username cannot contain '@'")
    if db_user:
        raise HTTPException(status_code=404, detail="Username already in use")
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=404, detail="Email already in use")

    hashed_password = CryptContext(schemes='bcrypt', deprecated="auto").hash(user.password)

    await create_user(db, user, hashed_password)

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


# @router.patch("/verify_email")
# async def verify_email(user: schemas.User = Depends(get_current_user), db=Depends(get_db)):
#
#     await verifyEmail(db, user.username)
#
#     return await create_token(user.username, hashed_password)


@router.post("/reset_password")
async def reset_password(username: schemas.ResetPassword, request: Request, db=Depends(get_db)):

    db_user = await get_user_from_username_or_email(username.username, db)
    if db_user is None:
        return HTTPException(status_code=404, detail="User not Found")

    with open(str(Path.cwd()) + "/templates/auth/email_templates/reset_password.html") as f:
        template_str = f.read()

    message = emails.html(subject=JinjaTemplate('Сброс пароля на сайте "Шахматы Будды"'),
                          html=JinjaTemplate(template_str),
                          mail_from=(settings.EMAIL_FROM_NAME, settings.EMAIL_FROM_EMAIL))

    token = await create_token(db_user.username, db_user.hashed_password)

    response = message.send(to=(db_user.username, db_user.email),
                            render={'token': token['access_token'],
                                    'username': db_user.username,
                                    'base_url': str(request.base_url),
                                    'hostname': request.url.hostname
                                    },
                            smtp={"host": settings.EMAIL_HOST, "port": settings.EMAIL_PORT})

    return HTMLResponse(str(response))

