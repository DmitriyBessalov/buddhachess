from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app.services.base_auth import OAuth2PasswordBearerCookie
from app.settings import settings
from app.models.user import table_user
from app.db import database

import jwt


async def create_token(username: str, hashed_password: str):
    token = jwt.encode({'username': username, 'hashed_password': hashed_password},
                       settings.JWT_SECRET,
                       algorithm=settings.JWT_ALGORITHM)

    return {"token_type": "bearer", "access_token": token, "username": username}


async def create_token_anonimous(username: str):
    token = jwt.encode({'username': username},
                       settings.JWT_SECRET,
                       algorithm=settings.JWT_ALGORITHM)

    return {"token_type": "bearer", "access_token": token, "username": username}


async def get_user_from_username_or_email(username: str):
    if username.find("@") != -1:
        db_user = await database.fetch_one(
            query=table_user.select().where(table_user.c.email == username)
        )
    else:
        db_user = await database.fetch_one(query=table_user.select().where(table_user.c.username == username))
    return db_user


async def get_current_user(
        token: str = Depends(OAuth2PasswordBearerCookie(tokenUrl="/api/auth/token")),
):
    try:
        if token is None:
            return {"group": "anonimous", "username": None}

        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])

        if payload["username"][:10] == "Anonimous_":
            return {"username": payload["username"],
                    "access_token": token,
                    "group": "anonimous",
                    }

        db_user = await database.fetch_one(query=table_user.select().where(table_user.c.username == payload["username"]))

        if db_user['hashed_password'] != payload["hashed_password"]:
            raise HTTPException(
                status_code=403, detail="Invalid Token"
            )
    except:
        return {"group": "anonimous", "username": None}

    return jsonable_encoder(db_user)

