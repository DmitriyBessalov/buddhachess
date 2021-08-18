from fastapi import APIRouter

from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/login")
async def get(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register")
async def get(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.get("/reset_activation")
async def get(request: Request):
    return templates.TemplateResponse("auth/reset_password.html", {"request": request})


@router.get("/account_verify/")
async def get(token: str):
    return templates.TemplateResponse("auth/account_verify.html", {"token": token})


@router.get("/reset_password/")
async def get(token: str):
    return templates.TemplateResponse("auth/reset_password.html", {"token": token})


@router.get("/password_confirm")
async def get(request: Request):
    return templates.TemplateResponse("auth/password_confirm.html", {"request": request})
