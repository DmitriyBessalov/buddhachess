from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi import Request

router = APIRouter()


@router.get("/")
async def get(request: Request):
    return HTMLResponse("<html>11</html>")
