from fastapi import FastAPI
import uvicorn
from apps.article.router import router as article_router
from apps.auth.router import router as auth_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from settings import settings

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"],)
app.include_router(article_router, prefix="/ru", tags=['article'])


@app.get("/")
async def redirect_home():
    return RedirectResponse("/ru/", status_code=302)

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )
