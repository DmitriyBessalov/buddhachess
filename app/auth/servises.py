from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.auth import schemas, models
from pathlib import Path
from settings import settings
from db import get_db
from emails.template import JinjaTemplate
import emails
import jwt


async def create_user(db: Session, user: schemas.UserRegister, hashed_password):
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def update_password(db: Session, username: str, hashed_password: str):
    user = db.query(models.User).filter_by(username=username).one()
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def create_token(username: str, hashed_password: str):
    token = jwt.encode({'username': username, 'hashed_password': hashed_password},
                       settings.JWT_SECRET,
                       algorithm=settings.JWT_ALGORITHM)

    return {"token_type": "bearer", "access_token": token, "username": username}


async def create_token_anonimous(username: str):
    token = jwt.encode({'username': username},
                       settings.JWT_SECRET,
                       algorithm=settings.JWT_ALGORITHM)

    return {"token_type": "bearer", "access_token_anonimous": token, "username": username}

async def get_user_from_username_or_email(username: str, db: Session):
    if username.find("@") != -1:
        db_user = db.query(models.User).filter(models.User.email == username).first()
    else:
        db_user = db.query(models.User).filter(models.User.username == username).first()
    return db_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


async def get_current_user(
    db=Depends(get_db),
    token: str = Depends(oauth2_scheme),
    anonimous: bool = False
):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])

        if anonimous:
            return {'username': payload["username"]}

        user = db.query(models.User).get(payload["username"])

        if user.hashed_password != payload["hashed_password"]:
            raise HTTPException(
                status_code=403, detail="Please refresh token"
            )
    except:
        raise HTTPException(
            status_code=403, detail="Invalid Token"
        )

    return schemas.UserHashPassword.from_orm(user)


async def get_current_user_with_anonimous(
        db=Depends(get_db),
        token: str = Depends(oauth2_scheme),
):
    return await get_current_user(db, token, True)


async def send_email(templates: str, title: str, request: Request, db_user: schemas.UserHashPassword):

    with open(str(Path.cwd()) + "/templates/auth/email_templates/" + templates + ".html") as f:
        template_str = f.read()

    message = emails.html(subject=JinjaTemplate(title),
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

    return str(response)


async def verify__email(username, db):
    user = db.query(models.User).filter_by(username=username).one()
    user.is_verified = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

