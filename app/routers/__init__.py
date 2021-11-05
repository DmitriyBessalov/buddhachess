from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles

from .api.v1.auth import router as router_auth_api
from .web.auth import router as router_auth
from .web.article import router as router_article
from .web.base import router as router_base
from .web.game import router as router_game
from .websocket.game import router as router_game_websocket


router = APIRouter()
router.include_router(router_base, prefix="", tags=['base'])
router.include_router(router_auth, prefix="/{lang}/auth", tags=["auth"],)
router.include_router(router_auth_api, prefix="/api/auth", tags=["auth_api"],)
router.include_router(router_article, prefix="/{lang}/docs", tags=['article'])
router.include_router(router_game, prefix="/{lang}/game", tags=['game'])
router.include_router(router_game_websocket, prefix="/ws/game", tags=['game_websocket'])
router.mount("/static", StaticFiles(directory="app/static"), name="static")
router.mount("/media", StaticFiles(directory="app/media"), name="media")
