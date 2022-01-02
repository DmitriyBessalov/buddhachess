from fastapi import APIRouter, Depends

from fastapi import Request
from fastapi.templating import Jinja2Templates
from services import auth as servises_auth
templates = Jinja2Templates(directory="app/templates")

router = APIRouter()


@router.get("/")
async def get(request: Request, lang: str, user=Depends(servises_auth.get_current_user)):
    return templates.TemplateResponse("game/create_game.html", {"request": request, "user": user})


@router.get("/{game_id}")
async def get(request: Request, lang: str, game_id: int, user=Depends(servises_auth.get_current_user)):
    return templates.TemplateResponse("game/game.html", {"request": request, "user": user})
