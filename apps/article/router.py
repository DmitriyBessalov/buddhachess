from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get(request: Request):
    return HTMLResponse("<html>11</html>")


@router.get("/article/{id}", response_class=HTMLResponse)
async def get(request: Request, id: str):
    return templates.TemplateResponse("base.html", {"request": request, "id": id})
