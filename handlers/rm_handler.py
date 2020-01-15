import logging

from sanic.response import json
from controllers.modify_handler import rm_handler as c_rm_handler
import models.errors as error_codes
from utils.http_helper import get_req_key
from resources import redis_set, redis_get
from controllers.wraps import admin_pwd

# http://localhost:8000/rm?web_path=/dynamic_hello
@admin_pwd
async def rm_handler(request):
    db_handler_list = await redis_get("db_handler_list")

    name = get_req_key(request, "name", "")
    web_path = get_req_key(request, "web_path", "")
    if not web_path:
        web_path = db_handler_list.get(name, {}).get("web_path", "")
        if not web_path:
            result = {
                "err": error_codes.svc_name_is_invalid,
                "err_msg": "web_path is empty"
            }
            return json(result)

    c_rm_handler(request.app, web_path)

    if name in db_handler_list:
        del db_handler_list[name]

    await redis_set("db_handler_list", 0, db_handler_list)

    result = {
        "err": 0,
    }
    return json(result)
