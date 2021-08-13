from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
import emails
from emails.template import JinjaTemplate
from settings import settings
from db import get_db
from .servises import create_user, create_token, get_user_by_username, get_user_by_email
from . import schemas
from pathlib import Path

router = APIRouter()


@router.post("/users", response_model=schemas.User, response_model_exclude_none=True)
async def user_create(
        request: Request,
        user: schemas.UserCreate,
        db=Depends(get_db),
):
    db_user = await get_user_by_username(user.username, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already in use")

    db_user = await get_user_by_email(user.email, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    user = await create_user(db, user)
    f = await create_token(user)
    return HTMLResponse(str(f))


@router.get("/test_email")
async def test_email():
    with open(Path("../../templates/auth/email_templates") / "reset_password.html") as f:
        template_str = f.read()

    message = emails.html(subject=JinjaTemplate('Payment Receipt No.{{ billno }}'),
                          html=JinjaTemplate('<p>Dear {{ name }}! This is a receipt...'),
                          mail_from=(settings.EMAIL_FROM_NAME, settings.EMAIL_FROM_EMAIL))


    response = message.send(to=('John Brown', 'noyato9573@cfcjy.com'),
                            render={'name': 'John Brown', 'billno': '141051906163'},
                            smtp={"host": settings.EMAIL_HOST, "port": settings.EMAIL_PORT})

    return HTMLResponse(str(response))

# @router.get(
#     "/users",
#     response_model=List[User],
#     response_model_exclude_none=True,
# )
# async def users_list(
#         response: Response,
#         db=Depends(get_db),
#         current_user=Depends(get_current_active_superuser),
# ):
#     """
#     Get all users
#     """
#     users = get_users(db)
#     # This is necessary for react-admin to work
#     response.headers["Content-Range"] = f"0-9/{len(users)}"
#     return users
#
#
# @router.get("/users/me", response_model=User, response_model_exclude_none=True)
# async def user_me(current_user=Depends(get_current_active_user)):
#     """
#     Get own user
#     """
#     return current_user
#
#
# @router.get(
#     "/users/{user_id}",
#     response_model=User,
#     response_model_exclude_none=True,
# )
# async def user_details(
#         request: Request,
#         user_id: int,
#         db=Depends(get_db),
#         current_user=Depends(get_current_active_superuser),
# ):
#     """
#     Get any user details
#     """
#     user = get_user(db, user_id)
#     return user
#     # return encoders.jsonable_encoder(
#     #     user, skip_defaults=True, exclude_none=True,
#     # )
#
#
# @router.put(
#     "/users/{user_id}", response_model=User, response_model_exclude_none=True
# )
# async def user_edit(
#         request: Request,
#         user_id: int,
#         user: UserEdit,
#         db=Depends(get_db),
#         current_user=Depends(get_current_active_superuser),
# ):
#     """
#     Update existing user
#     """
#     return edit_user(db, user_id, user)
#
#
# @router.delete(
#     "/users/{user_id}", response_model=User, response_model_exclude_none=True
# )
# async def user_delete(
#         request: Request,
#         user_id: int,
#         db=Depends(get_db),
#         current_user=Depends(get_current_active_superuser),
# ):
#     """
#     Delete existing user
#     """
#     return delete_user(db, user_id)
