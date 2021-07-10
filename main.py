from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
import uvicorn
from apps.article.router import router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from settings import settings


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router, prefix="/game")

if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )


# @app.get("/")
# async def get(request: Request):
#     return HTMLResponse("<html>/root</html>")
#
#
# @app.get("/test_template/{id}", response_class=HTMLResponse)
# async def get(request: Request, id: str):
#     return templates.TemplateResponse("base.html", {"request": request, "id": id})
