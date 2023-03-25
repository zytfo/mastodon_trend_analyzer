# stdlib
from typing import Any, Optional

# thirdparty
import orjson
from sanic.response import JSONResponse, json

from app.core.helpers import base_models


# project


def on_write_error(errors: Any, status: int = 500) -> JSONResponse:
    body = base_models.ErrorResponse(errors=errors)
    return json(body.dict(), dumps=orjson.dumps, status=status)  # noqa


def on_write_data(result: Any, status: int = 200) -> JSONResponse:
    body = base_models.BaseResponse(
        result=result,
        success=True,
    )
    return json(body.dict(), dumps=orjson.dumps, status=status)  # noqa


def on_write_json(
    result: Any, total_count: int, limit: Optional[int] = None, offset: Optional[int] = None, status: int = 200
) -> JSONResponse:
    body = base_models.PagingResponse(result=result, success=True, limit=limit, offset=offset, total_count=total_count)
    return json(body.dict(), dumps=orjson.dumps, status=status)  # noqa
