from functools import wraps
import srvconf
from utils.http_helper import get_req_key
from sanic.response import json


def admin_pwd(f):
    @wraps(f)
    async def _run(request, *args):
        if srvconf.admin_pwd:
            pwd = get_req_key(request, "admin_pwd", "")
            if pwd != srvconf.admin_pwd:
                return json({"err": 1, "err_msg": "pwd is not correct"})
        rsp = await f(request)
        return rsp
    return _run
