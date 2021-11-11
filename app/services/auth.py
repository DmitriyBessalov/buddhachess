from fastapi import Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from app.services.base_auth import OAuth2PasswordBearerCookie
from starlette.responses import RedirectResponse

from app.models.user import User
from app.settings import settings

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

    return {"token_type": "bearer", "access_token_anonimous": token, "username": username}


async def get_user_from_username_or_email(username: str):
    if username.find("@") != -1:
        db_user = await User.objects.get_or_none(email=username)
    else:
        db_user = await User.objects.get_or_none(username=username)
    return db_user

oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/api/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    anonimous: bool = False,
):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])

        if anonimous:
            return {'username': payload["username"],
                    'access_token_anonimous': token}

        db_user = await User.objects.get(username=payload["username"])

        if db_user.hashed_password != payload["hashed_password"]:
            return RedirectResponse("/auth/login", status_code=302)
    except:
        raise HTTPException(
            status_code=403, detail="Invalid Token"
        )

    return jsonable_encoder(db_user)


async def get_current_user_with_anonimous(
        token: str = Depends(oauth2_scheme),
):
    return await get_current_user(token, True)


