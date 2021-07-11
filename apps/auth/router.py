from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from settings import settings
from .schemas import User, UserCreate, UserUpdate, UserDB
from fastapi_users.db import SQLAlchemyUserDatabase
from .models import users
import databases

router = APIRouter()

database = databases.Database(settings.database_url)

user_db = SQLAlchemyUserDatabase(UserDB, database, users)


jwt_authentication = JWTAuthentication(secret=settings.jwt_secret, lifetime_seconds=3600)

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

router.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix="/auth/jwt",
)
