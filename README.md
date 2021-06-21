[![Test](https://github.com/NexSabre/fastapi-jinja/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/NexSabre/fastapi-jinja/actions/workflows/tests.yml)
[![PyPI version](https://badge.fury.io/py/fastapi-jinja.svg)](https://badge.fury.io/py/fastapi-jinja)

# fastapi-jinja

Adds integration of the Jinja template language to FastAPI. This is inspired and based off fastapi-chamelon by Mike Kennedy. Check that out, if you are using chamelon.

Originall code [mikeckennedy/fastapi-chameleon](https://github.com/mikeckennedy/fastapi-chameleon)

Forked from [AGeekInside/fastapi-jinja](https://github.com/AGeekInside/fastapi-jinja). The repository looks out of date, there are a few issues left.

## Installation
Now, you can install `fastapi-jinja` using a pip

```bash
pip install fastapi-jinja
```

## Usage

This is easy to use. Just create a folder within your web app to hold the templates such as:

```
├── main.py
├── views.py
│
├── templates
│   ├── home
│   │   └── index.j2
│   └── shared
│       └── layout.j2

```

In the app startup, tell the library about the folder you wish to use:

```python
import os
import fastapi_jinja

dev_mode = True

folder = os.path.dirname(__file__)
template_folder = os.path.join(folder, 'templates')
template_folder = os.path.abspath(template_folder)

fastapi_jinja.global_init(template_folder, auto_reload=dev_mode)
```

Then just decorate the FastAPI view methods (works on sync and async methods):

```python
from fastapi_jinja import template

@router.post("/")
@template('home/index.j2')
async def home_post(request: Request):
    form = await request.form()
    vm = PersonViewModel(**form)

    return vm.dict() # {'first':'John', 'last':'Doe', ...}

```

The view method should return a `dict` to be passed as variables/values to the template.
We can also return model objects that can be converted into a dictionary, common when using libraries
such as pydantic to represent models in various forms.

```python
from fastapi_jinja import template
from pydantic import BaseModel

class Person(BaseModel):
    id: int
    name: str

@router.post("/")
@template('home/index.j2')
async def home_post(request: Request):
    form = await request.form() # form: {'id': 1, 'name': 'Jane'}
    person = Person(**form)

    return person # Person(id=1, name='Jane')

```

If a `fastapi.Response` is returned, the template is skipped and the response along with status_code and
other values is directly passed through. This is common for redirects and error responses not meant
for this page template.
