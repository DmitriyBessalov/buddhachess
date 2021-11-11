from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def HTTP_Error(loc: str, msg: str):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=jsonable_encoder({
            "detail": [{
                "loc": ["", loc],
                "msg": msg
            }]
        }),
    )
