import logging

from sanic.response import json

from controllers.modify_handler import add_handler as c_add_handler

from utils.http_helper import get_req_key
from resources import redis_set, redis_get
import datetime


async def add_handler(request):
    # http://localhost:8000/add?name=dynamic_hello&func=dynamic_hello&code=xxx&web_path=xxx
    name = get_req_key(request, "name")
    func = get_req_key(request, "func")
    code = get_req_key(request, "code")
    web_path = get_req_key(request, "web_path")

    # c_add_handler(request.app, name, func, code, web_path)

    db_handler_list = await redis_get("db_handler_list")
    if name not in db_handler_list:
        handler_info = {
            "name": name,
            "file_path": "",
            "func": func,
            "web_path": web_path,
            "code": code,
            "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        db_handler_list[name] = handler_info
    else:
        db_handler_list[name]['code'] = code

    await redis_set("db_handler_list", 0, db_handler_list)

    ret = {
        "err": 0,
    }
    return json(ret)
