import json as sysjson
import logging
import traceback

from sanic import Sanic
from sanic.response import json
import asyncio
import srvconf
import models.errors as errors
from utils.http_helper import json_result
from sanic.exceptions import NotFound

app = Sanic(__name__)

from controllers.sync_system_handler import Sync

sync = Sync(app)

@app.exception(NotFound)
def ignore_404(request, exception):
    return json({"err": errors.svc_is_not_found, "err_msg": "not found"}, status=404)

@app.exception(Exception)
def ignore_500s(request, exception):
    error_info = "system_error {}\n".format(type(exception))
    error_info += traceback.format_exc()
    logging.error(error_info)
    return json({"err": errors.system_error, "err_msg": error_info})


@app.listener('before_server_start')
async def setup(app, loop):
    await sync.init()
    loop.create_task(sync.sync())


@app.listener('after_server_stop')
async def close_service(app, loop):
    await sync.close()

