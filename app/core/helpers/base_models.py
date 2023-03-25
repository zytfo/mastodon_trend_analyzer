# stdlib
from typing import Any, Optional

# thirdparty
from pydantic import BaseModel, Field
from sanic_ext.extensions.openapi import definitions, openapi


class BaseResponse(BaseModel):
    result: Any
    success: bool

    @classmethod
    def get_response_definitions(cls):
        return [
            definitions.Response(
                {"application/json": openapi.Component(cls)},
                status=200,
            ),
            definitions.Response(
                {"application/json": openapi.Component(ErrorResponse)},
                status=422,
                description="Validation error",
            ),
        ]


class BaseRequestBody(BaseModel):
    @classmethod
    def get_body_definition(cls):
        return {"application/json": openapi.Component(cls)}


class BaseRequestQuery(BaseModel):
    @classmethod
    def get_query_definitions(cls):
        result = []
        for k, v in cls.__fields__.items():
            result.append(definitions.Parameter(name=k, schema=v.type_, required=v.required))  # noqa
        return result


class PagingResponse(BaseResponse):
    limit: Optional[int] = Field(default=1000)
    offset: Optional[int] = Field(default=0)
    total_count: Optional[int] = Field(default=None)


class ErrorResponse(BaseModel):
    errors: Any
    success: bool = Field(default=False)
