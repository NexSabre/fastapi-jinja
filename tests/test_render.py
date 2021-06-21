import asyncio
import os

import fastapi
# noinspection PyPackageRequirements
import pytest
from jinja2.exceptions import TemplateNotFound
from starlette.requests import Request

import fastapi_jinja as fj

here = os.path.dirname(__file__)
folder = os.path.join(here, "templates")

fake_request = Request(scope={'type': 'http'})

class DictModel:
    """This represents a model that can be converted into a dict, such as pydantic."""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
        }


def test_cannot_decorate_missing_template():
    with pytest.raises(TemplateNotFound):

        @fj.template("home/missing.j2")
        def view_method(request: Request):
            return {}

        view_method(fake_request)


def test_can_decorate_with_dictable_response():
    @fj.template("home/index.j2")
    def view_method(request: Request, name, age):
        model = DictModel(name, age)
        return model.to_dict()

    resp = view_method(fake_request, "foo", 42)
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 200


def test_can_decorate_dict_sync_method():
    @fj.template("home/index.j2")
    def view_method(request: Request, a, b, c):
        return {"a": a, "b": b, "c": c}

    resp = view_method(fake_request, 1, 2, 3)
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 200


def test_can_decorate_dict_async_method():
    @fj.template("home/index.j2")
    async def view_method(request: Request, a, b, c):
        return {"a": a, "b": b, "c": c}

    resp = asyncio.run(view_method(fake_request, 1, 2, 3))
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 200


def test_direct_response_pass_through():
    @fj.template("home/index.j2")
    def view_method(request: Request, a, b, c):
        return fastapi.Response(content="abc", status_code=418)

    resp = view_method(fake_request, 1, 2, 3)
    assert isinstance(resp, fastapi.Response)
    assert resp.status_code == 418
    assert resp.body == b"abc"
