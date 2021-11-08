from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def get(request: Request):
    return templates.TemplateResponse("docs/docs.html", {"request": request})


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
