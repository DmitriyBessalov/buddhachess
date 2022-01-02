from fastapi import Request
from pathlib import Path
from settings import settings
from services.auth import create_token
from emails.template import JinjaTemplate
import emails


async def send_email(
        templates: str,
        title: str,
        request: Request,
        username,
        email,
        hashed_password
):
    with open(str(Path.cwd()) + "/app/templates/auth/email_templates/" + templates + ".html") as f:
        template_str = f.read()

    message = emails.html(subject=JinjaTemplate(title),
                          html=JinjaTemplate(template_str),
                          mail_from=(settings.EMAIL_FROM_NAME, settings.EMAIL_FROM_EMAIL))

    token = await create_token(username, hashed_password)

    response = message.send(to=(username, email),
                            render={'token': token['access_token'],
                                    'username': username,
                                    'base_url': str(request.base_url),
                                    'hostname': request.url.hostname
                                    },
                            smtp={"host": settings.EMAIL_HOST, "port": settings.EMAIL_PORT})
    return str(response)
