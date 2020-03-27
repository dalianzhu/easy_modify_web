from sanic.response import json

import models.db
import utils.time
from controllers.wraps import admin_pwd
from utils.http_helper import get_req_key


@admin_pwd
async def add_handler(request):
    # http://localhost:8000/add?name=dynamic_hello&code=xxx&web_path=xxx
    name = get_req_key(request, "name")
    code = get_req_key(request, "code")
    web_path = get_req_key(request, "web_path")

    db = models.db.FileDB()
    tp = models.db.FuncItem()
    tp.name = name
    tp.file_path = ""
    tp.type = "user"
    tp.web_path = web_path
    tp.last_update = utils.time.now_str()
    tp.code = code
    db.set(name, tp)

    ret = {
        "err": 0,
    }
    return json(ret)
