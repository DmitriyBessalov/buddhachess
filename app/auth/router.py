from fastapi import APIRouter

from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/login")
async def get(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/registr")
async def get(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.get("/reset_activation")
async def get(request: Request):
    return templates.TemplateResponse("auth/reset_activation.html", {"request": request})


@router.get("/reset_password/")
async def get(token: str):
    return templates.TemplateResponse("auth/reset_password.html", {"token": token})


@router.get("/reset_password_confirm")
async def get(request: Request):
    return templates.TemplateResponse("auth/reset_password_confirm.html", {"request": request})
