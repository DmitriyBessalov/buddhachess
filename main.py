from fastapi import FastAPI
import uvicorn
from app.article.router import router as article_router
from app.auth.router import router as auth_router

from app.auth.api import router as auth_api_router

from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from settings import settings
import subprocess

app = FastAPI()

app.include_router(auth_api_router, prefix="/api/users", tags=["users_api"],)
app.include_router(auth_router, prefix="/auth", tags=["auth"],)
app.include_router(article_router, prefix="/ru", tags=['article'])


@app.get("/")
async def redirect_home():
    return RedirectResponse("/ru/", status_code=302)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/git_update")
async def redirect_home():
    result = subprocess.run('git reset --hard origin/master && git pull https://github.com/DmitriyBessalov/buddhachess.git', shell=True, stdout=subprocess.PIPE)
    return HTMLResponse(result.stdout)


@app.get("/robots.txt")
async def redirect_home():
    return HTMLResponse("User-agent * \nDisallow /")

if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
    )
