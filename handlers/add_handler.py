from sanic.response import json
import logging

import models.db
import models.errors
import utils.time
from controllers.wraps import admin_pwd
from utils.http_helper import get_req_key
import types
from models.errors import system_error_ret
from sanic import Sanic
import traceback

tp_app = Sanic(__name__)


def _check_code(name: str, code: str, web_path: str) -> str:
    try:
        md = types.ModuleType(name)
        exec(code, md.__dict__)

        http_handler = getattr(md, name)
        tp_app.add_route(http_handler, web_path, methods={
            "GET", "POST"}, name=name)
        try:
            tp_app.remove_route(web_path)
        except:
            pass
        try:
            tp_app.remove_route(web_path + "/")
        except:
            pass
        return ""
    except Exception as err:
        return traceback.format_exc()


@admin_pwd
async def add_handler(request):
    # http://localhost:8000/add?name=dynamic_hello&code=xxx&web_path=xxx
    name = get_req_key(request, "name")
    code = get_req_key(request, "code")
    web_path = get_req_key(request, "web_path")
    logging.debug("add_handler name:{} code:{} web_path:{}".format(name, code, web_path))

    err = _check_code(name, code, web_path)
    if err != "":
        ret = {
            "err": models.errors.code_is_incorrect,
            "err_msg": err
        }
        return json(ret)

    db = models.db.FileDB()
    tp = db.get(name)
    if tp:
        if tp.type == "system":
            return system_error_ret("{} is a system func".format(tp.name))
    else:
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
