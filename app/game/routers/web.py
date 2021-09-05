from fastapi import APIRouter

from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/game/start")
async def get(request: Request, lang: str):
    return templates.TemplateResponse("game/start.html", {"request": request})


@router.get("/game/<game_id>")
async def get(request: Request, lang: str, game_id: int):
    return templates.TemplateResponse("game/game.html", {"request": request})
