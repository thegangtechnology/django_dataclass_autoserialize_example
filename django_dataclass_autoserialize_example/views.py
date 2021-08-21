from __future__ import annotations
from django_dataclass_autoserialize import AutoSerialize, swagger_post_schema, swagger_get_schema
from dataclasses import dataclass

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


@dataclass
class InputParam(AutoSerialize):
    a: int
    b: int

    @classmethod
    def example(cls) -> InputParam:
        # this is actually optional but it will show up
        # in swagger doc
        return cls(a=3, b=2)


@dataclass
class ComputeResponse(AutoSerialize):
    msg: str
    result: int

    @classmethod
    def example(cls) -> ComputeResponse:
        return cls(msg='hello world', result=5)


class AddView(APIView):

    @swagger_post_schema(
        body_type=InputParam,
        response_types={200: ComputeResponse}
    )
    def post(self, request: Request) -> Response:
        param = InputParam.from_post_request(request)
        return ComputeResponse(msg='add successfully',
                               result=param.a + param.b).to_response()


class SubtractView(APIView):
    @swagger_get_schema(
        query_type=InputParam,
        response_types={200: ComputeResponse}
    )
    def get(self, request: Request) -> Response:
        param = InputParam.from_get_request(request)
        return ComputeResponse(msg='subtract successfully',
                               result=param.a - param.b).to_response()
