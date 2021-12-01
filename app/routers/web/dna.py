from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()


@router.get("/")
async def redirect_home(request: Request):
    return templates.TemplateResponse("dna.html", {"request": request})
