import uvicorn
from fastapi import FastAPI
from db import database
from settings import settings
from fastapi.staticfiles import StaticFiles
from app.routers.api.v1.auth import router as router_auth_api
from app.routers.web.auth import router as router_auth
from app.routers.web.article import router as router_article
from app.routers.web.base import router as router_base
# from .web.game import router as router_game
# from .websocket.game import router as router_game_websocket


app = FastAPI()
app.state.database = database
app.include_router(router_base, prefix="", tags=['base'])
app.include_router(router_auth, prefix="/{lang}/auth", tags=["auth"],)
app.include_router(router_auth_api, prefix="/api/auth", tags=["auth_api"],)
app.include_router(router_article, prefix="/{lang}/docs", tags=['article'])
# app.include_router(router_game, prefix="/{lang}/game", tags=['game'])
# app.include_router(router_game_websocket, prefix="/ws/game", tags=['game_websocket'])
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/media", StaticFiles(directory="app/media"), name="media")


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
        use_colors=True,
    )
