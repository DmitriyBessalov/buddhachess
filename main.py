from fastapi import FastAPI
import uvicorn
from apps.article.router import router as article_router
from apps.auth.router import router as auth_router
from fastapi.staticfiles import StaticFiles
from settings import settings

app = FastAPI()

app.include_router(article_router, prefix="/game", tags=['game'])
app.include_router(auth_router, prefix="/users", tags=["auth"],)

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )

