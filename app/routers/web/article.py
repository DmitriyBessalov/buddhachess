from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.services import auth as servises_auth

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def get(request: Request, user=Depends(servises_auth.get_current_user_check)):
    return templates.TemplateResponse("docs/docs.html", {"request": request, "user": user['username']})


@router.get("/in-yan")
async def get(request: Request):
    return templates.TemplateResponse("docs/in-yan.html", {"request": request})


@router.get("/flang")
async def get(request: Request):
    return templates.TemplateResponse("docs/flang.html", {"request": request})


@router.get("/in-yan_flang")
async def get(request: Request):
    return templates.TemplateResponse("docs/in-yan_flang.html", {"request": request})


@router.get("/in-yan_fib")
async def get(request: Request):
    return templates.TemplateResponse("docs/in-yan_fib.html", {"request": request})
