from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates

from services import auth as servises_auth

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get(request: Request, user=Depends(servises_auth.get_current_user)):
    return templates.TemplateResponse("docs/docs.html", {"request": request, "user": user})


@router.get("/in-yan")
async def get(request: Request, user=Depends(servises_auth.get_current_user)):
    return templates.TemplateResponse("docs/in-yan.html", {"request": request, "user": user})


@router.get("/flang")
async def get(request: Request, user=Depends(servises_auth.get_current_user)):
    return templates.TemplateResponse("docs/flang.html", {"request": request, "user": user})


@router.get("/in-yan_flang")
async def get(request: Request, user=Depends(servises_auth.get_current_user)):
    return templates.TemplateResponse("docs/in-yan_flang.html", {"request": request, "user": user})


@router.get("/in-yan_fib")
async def get(request: Request, user=Depends(servises_auth.get_current_user)):
    return templates.TemplateResponse("docs/in-yan_fib.html", {"request": request, "user": user})
