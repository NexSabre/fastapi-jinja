import pytest

import fastapi_jinja as fj
from fastapi_jinja.exceptions import FastAPIJinjaException


def test_missing_request_argument():
    with pytest.raises(FastAPIJinjaException):

        @fj.template("home/index.j2")
        def view_method():
            return {}
