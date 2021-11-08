import datetime

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from sqlalchemy import func

from db import get_session

templates = Jinja2Templates(directory="templates")

router = APIRouter()


def title(_app):
    title = {
        'user': 'Пользователи',
        'game': 'Игры',
    }
    return title[_app]


@router.get("/administration/{app}")
async def _app(request: Request, app: str):
    if app == 'null':
        return {}

    if app != 'statistic':
        uri = 'base'
    else:
        uri = 'statistic'

    response = templates.TemplateResponse("administration/" + uri + ".html", {
        "request": request,
        "title": title(app),
        "app": app,
        # "current_user": current_user
    })
    response.set_cookie(key="Authorization", value=request.cookies['Authorization'], max_age=604800, httponly=True)
    return response


@router.get("/administration/{app}/edit")
async def edit(
        request: Request,
        app: str, pk: str = None,
        # current_user=Depends(get_current_admin_user),
        db=Depends(get_session)):
    if pk:
        action = 'Редактировать'
    else:
        action = 'Создать'

    author = dict()
    story_rubric = dict()
    tags = dict()
    last_date = datetime.date.today()


    return templates.TemplateResponse("adminpanel/" + app + "_edit.html", context={
        'pk': pk,
        'app': app,
        'title': action + ' ' + title(app),
        'author': author,
        'story_rubric': story_rubric,
        'tags': tags,
        'last_date': last_date,
        'request': request,
        # "current_user": current_user
    })