# import subprocess
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/")
async def redirect_home():
    return RedirectResponse("/ru/docs/", status_code=302)


# @router.get("/admin")
# async def get(request: Request):
#     return templates.TemplateResponse("admin/base.html", {"request": request})


# @router.post("/git_update")
# async def redirect_home():
#     result = subprocess.run('git reset --hard origin/master && git pull https://github.com/DmitriyBessalov/buddhachess.git', shell=True, stdout=subprocess.PIPE)
#     return HTMLResponse(result.stdout)


@router.get("/robots.txt")
async def redirect_home():
    return HTMLResponse("User-agent * \nAllow /")

