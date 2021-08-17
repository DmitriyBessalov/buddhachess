from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
import emails
from emails.template import JinjaTemplate
from passlib.context import CryptContext

from app.auth.servises import get_user_from_username_or_email, create_user, get_current_user

from settings import settings
from db import get_db
import jwt

from app.auth import schemas
from app.auth import models
from fastapi.security import OAuth2PasswordBearer

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

    token = jwt.encode(
        {'username': user.username, 'password': hashed_password},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return {'token_type': 'bearer', 'access_token': token}


@router.post("/token")
async def login(user: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):

    db_user = await get_user_from_username_or_email(user.username, db)
    if db_user is None:
        return HTTPException(status_code=404, detail="User not Found")

    if CryptContext(schemes='bcrypt', deprecated="auto").verify(user.password, db_user.hashed_password):

        token = jwt.encode(
            {'username': db_user.username, 'password': db_user.hashed_password},
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )
        token = {"token_type": 'bearer', 'access_token': token}
        return token
    return HTTPException(status_code=404, detail="Wrong password")


@router.patch("/password")
async def password_update(user: schemas.User = Depends(get_current_user)):
    return HTMLResponse((str(user)))


# @router.post("/reset_activation")
# async def reset_activation(user: schemas.ResetActivation, db=Depends(get_db)):
#     with open(Path("../../templates/auth/email_templates") / "reset_password.html") as f:
#         template_str = f.read()
#
#     message = emails.html(subject=JinjaTemplate('Payment Receipt No.{{ billno }}'),
#                           html=JinjaTemplate('<p>Dear {{ name }}! This is a receipt...'),
#                           mail_from=(settings.EMAIL_FROM_NAME, settings.EMAIL_FROM_EMAIL))
#
#
#     response = message.send(to=('John Brown', user.email),
#                             render={'name': 'John Brown', 'billno': '141051906163'},
#                             smtp={"host": settings.EMAIL_HOST, "port": settings.EMAIL_PORT})
#
#     return HTMLResponse(str(response))
#
