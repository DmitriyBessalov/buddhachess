import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.base.routers import router as router_base
from app.auth.routers.web import router as router_auth
from app.auth.routers.api import router as router_auth_api
from app.article.routers.web import router as router_article
from app.game.routers.web import router as router_game
from app.game.routers.websocket import router as router_game_websocket
from settings import settings

app = FastAPI()
app.include_router(router_base, prefix="", tags=['base'])
app.include_router(router_auth, prefix="/{lang}/auth", tags=["auth"],)
app.include_router(router_auth_api, prefix="/api/auth", tags=["auth_api"],)
app.include_router(router_article, prefix="/{lang}/docs", tags=['article'])
app.include_router(router_game, prefix="/{lang}/game", tags=['game'])
app.include_router(router_game_websocket, prefix="/ws/game", tags=['game_websocket'])
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
    )
