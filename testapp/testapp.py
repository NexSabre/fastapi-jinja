import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

import fastapi_jinja


app = FastAPI()

folder = os.path.dirname(__file__)
template_folder = os.path.join(folder, "templates")
print(template_folder)
static_folder = os.path.join(template_folder, "static")
print(static_folder)

app.mount("/static", StaticFiles(directory=static_folder), name="static")
fastapi_jinja.global_init(template_folder)


@app.get("/")
@fastapi_jinja.template("test.html")
async def root(request: Request):
    render_dict = {
        "title": "Test Title",
    }

    user_ids = ["user-" + str(i) for i in range(10)]

    users = [{"url": f"http://site/{user}", "username": user} for user in user_ids]

    render_dict["users"] = users

    return render_dict, request
