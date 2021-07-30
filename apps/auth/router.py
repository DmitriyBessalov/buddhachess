from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from settings import settings
from .schemas import User, UserCreate, UserUpdate, UserDB
from fastapi_users.db import SQLAlchemyUserDatabase
from .models import users
import databases
from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

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
    fastapi_users.get_register_router(),
    prefix="/api",
)

router.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix="/api",
)

router.include_router(
    fastapi_users.get_reset_password_router(settings.jwt_secret),
    prefix="/api",
)

router.include_router(
    fastapi_users.get_users_router(),
    prefix="/api/users",
)


router.include_router(
    fastapi_users.get_verify_router(settings.jwt_secret),
    prefix="/api",
)


@router.on_event("startup")
async def startup():
    await database.connect()


@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@router.get("/login")
async def get(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/registr")
async def get(request: Request):
    return templates.TemplateResponse("auth/registr.html", {"request": request})


@router.get("/reset_activation")
async def get(request: Request):
    return templates.TemplateResponse("auth/reset_activation.html", {"request": request})


@router.get("/reset_password")
async def get(request: Request):
    return templates.TemplateResponse("auth/reset_password.html", {"request": request})


@router.get("/reset_password_confirm")
async def get(request: Request):
    return templates.TemplateResponse("auth/reset_password_confirm.html", {"request": request})
