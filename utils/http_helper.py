import datetime
import json
import logging
import os
import traceback
from functools import wraps

import aiohttp
from sanic.response import json as sjson
import models.errors


def trace(only_exception=True):
    def decorator(f):
        @wraps(f)
        async def run(request, *args):
            try:
                response = await f(request, *args)

                if not only_exception:
                    err_msg = ""
                    traceinfo = request.get("_traceinfo", [])
                    for line in traceinfo:
                        err_msg += "TRACE:{}\n".format(line)

                    body = json.loads(response.body)
                    body['_trace'] = err_msg
                    return sjson(body)

                return response
            except:
                logging.error("trace err!\n" + traceback.format_exc())
                err_msg = traceback.format_exc() + "\n"

                traceinfo = request.get("_traceinfo", [])
                for line in traceinfo:
                    err_msg += "TRACE:{}\n".format(line)
                return sjson({"err": models.errors.system_error, "err_msg": err_msg})

        return run

    return decorator


def tdebug(request, info):
    traceinfo = request.get("_traceinfo", [])
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    traceinfo.append("{} {}".format(now, info))
    request["_traceinfo"] = traceinfo


def get_req_key(request, key, default=None):
    result = default
    if key in request.args:
        result = request.args[key][0]
    elif key in request.form:
        result = request.form[key][0]
    else:
        try:
            body = json.loads(request.body)
            if key in body:
                result = body[key]
        except:
            pass

    if default is not None:
        try:
            if not isinstance(result, type(default)):
                result = type(default)(result)
        except:
            return default

    return result


def _get_real_body(request):
    if "bodycache" in request:
        return request['bodycache']

    try:
        body = json.loads(request.body)
        request['bodycache'] = body
    except:
        # logging.debug("body {}".format(body))
        logging.debug("decode body failed set emtpy")
        request['bodycache'] = {}
    return request['bodycache']


def get_body(request):
    try:
        return _get_real_body(request)['data']
    except Exception as err:
        logging.error(err)
        return {}


def get_env(request, key):
    # try:
    body = _get_real_body(request)
    # logging.debug("get_env body {}".format(body))
    return body['env'][key]
    # except Exception as err:
    #     logging.error(traceback.format_exc())
    #     return ""


def set_env(request, key: str, val: str):
    try:
        if 'bodycache' not in request:
            request['bodycache'] = {}

        if "env" not in request['bodycache']:
            request['bodycache']['env'] = {}

        request['bodycache']["env"][key] = val
        logging.debug("bodycache {}".format(request['bodycache']))

    except Exception as err:
        logging.error(traceback.format_exc())


def json_result(data, env=None):
    body = {"data": data, "env": env}
    return sjson(body)


async def post_json(url, data=None, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, timeout=50, data=data, headers=headers) as response:
            # logging.debug('post_json url {}, data {}'.format(url, data))
            ret = await response.text()
            # logging.debug('post_json url {}, ret {}'.format(url, ret))
            return json.loads(ret, encoding='utf-8')


@trace()
async def _test_trace(request):
    tdebug(request, "hello trace")
    raise Exception("err!")


async def _test():
    ret = await _test_trace({})
    print("test {}".format(ret))


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_test())
