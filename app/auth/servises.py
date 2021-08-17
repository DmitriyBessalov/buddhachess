from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from starlette import status
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


async def create_token(user: schemas.UserWithEmail):
    user_obj = schemas.UserWithEmail.from_orm(user)
    token = jwt.encode(user_obj.dict(), settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
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
    except:
        raise HTTPException(
            status_code=401, detail="Invalid Token"
        )

    return schemas.User2.from_orm(user)

# async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(
#             token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
#         )
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         permissions: str = payload.get("permissions")
#         token_data = schemas.TokenData(username=username, permissions=permissions)
#     except PyJWTError:
#         raise credentials_exception
#     user = get_user_from_username_or_email(token_data.username, db)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(
#         current_user: models.User = Depends(get_current_user),
# ):
#     if not current_user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# async def get_current_active_superuser(
#         current_user: models.User = Depends(get_current_user),
# ) -> models.User:
#     if not current_user.is_superuser:
#         raise HTTPException(
#             status_code=403, detail="The user doesn't have enough privileges"
#         )
#     return current_user
#
#
# def authenticate_user(db, email: str, password: str):
#     user = get_user_by_email(db, email)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user


# def sign_up_new_user(db, email: str, password: str):
#     user = get_user_by_email(db, email)
#     if user:
#         return False  # User already exists
#     new_user = create_user(
#         db,
#         schemas.UserCreate(
#             email=email,
#             password=password,
#             is_active=True,
#             is_superuser=False,
#         ),
#     )
#     return new_user
#
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#
# def create_access_token(*, data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
#     return encoded_jwt



# def get_user(db: Session, user_id: int):
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# def get_user_by_email(db: Session, email: str) -> schemas.UserBase:
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(
#         db: Session, skip: int = 0, limit: int = 100
# ) -> List[schemas.UserOut]:
#     return db.query(models.User).offset(skip).limit(limit).all()


# def delete_user(db: Session, user_id: int):
#     user = get_user(db, user_id)
#     if not user:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
#     db.delete(user)
#     db.commit()
#     return user


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