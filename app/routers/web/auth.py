from fastapi import APIRouter

from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

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


@router.get("/verify_activation/{token}")
async def get(token: str, request: Request):

    return templates.TemplateResponse('auth/verify_activation.html', context={'token': token, 'request': request})


@router.get("/reset_password")
async def get(request: Request):
    return templates.TemplateResponse("auth/reset_password.html", {"request": request})


@router.get("/password_confirm/{token}")
async def get(token: str, request: Request):
    return templates.TemplateResponse("auth/password_confirm.html", context={'token': token, 'request': request})
