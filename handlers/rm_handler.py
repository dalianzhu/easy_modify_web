from sanic.response import json

import models.db
from controllers.wraps import admin_pwd
from utils.http_helper import get_req_key


# http://localhost:8000/rm?name=dynamic_hello
@admin_pwd
async def rm_handler(request):
    name = get_req_key(request, "name")
    db = models.db.FileDB()
    db.rm(name)

    result = {
        "err": 0,
    }
    return json(result)
