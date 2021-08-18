from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db import get_db
from app.auth import schemas, models
import jwt
from settings import settings


async def create_user(db: Session, user: schemas.UserWithEmail, hashed_password):
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
    q = db.query(models.User).filter_by(username=username).one()
    q.hashed_password = hashed_password
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


async def create_token(username: str, hashed_password: str):
    token = jwt.encode({'username': username, 'hashed_password': hashed_password},
                       settings.JWT_SECRET,
                       algorithm=settings.JWT_ALGORITHM)

    return dict(token_type="bearer", access_token=token)


async def get_user_from_username_or_email(username: str, db: Session):
    if username.find("@") != -1:
        db_user = db.query(models.User).filter(models.User.email == username).first()
    else:
        db_user = db.query(models.User).filter(models.User.username == username).first()
    return db_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")


async def get_current_user(
    db=Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["username"])

        if user.hashed_password != payload["hashed_password"]:
            raise HTTPException(
                status_code=401, detail="Please refresh token"
            )
    except:
        raise HTTPException(
            status_code=401, detail="Invalid Token"
        )

    return schemas.UserHashPassword.from_orm(user)




# def edit_user(
#         db: Session, user_id: int, user: schemas.UserEdit
# ) -> schemas.User:
#     db_user = get_user(db, user_id)
#     if not db_user:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
#     update_data = user.dict(exclude_unset=True)
#
#     if "password" in update_data:
#         update_data["hashed_password"] = get_password_hash(user.password)
#         del update_data["password"]
#
#     for key, value in update_data.items():
#         setattr(db_user, key, value)
#
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user