import uvicorn
from fastapi import FastAPI
from settings import settings
from fastapi.staticfiles import StaticFiles
from routers.api.v1.auth import router as router_auth_api
from routers.web.auth import router as router_auth
from routers.web.article import router as router_article
from routers.web.base import router as router_base
from routers.web.game import router as router_game
from routers.websocket.game import router as router_game_websocket
from db import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(router_base, prefix="", tags=['base'])
app.include_router(router_auth, prefix="/{lang}/auth", tags=["auth"],)
app.include_router(router_auth_api, prefix="/api/auth", tags=["auth_api"],)
app.include_router(router_article, prefix="/{lang}/docs", tags=['article'])
app.include_router(router_game, prefix="/{lang}/game", tags=['game'])
app.include_router(router_game_websocket, prefix="/ws/game", tags=['game_websocket'])
app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/media", StaticFiles(directory="media"), name="media")


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
        use_colors=True,
    )
