import json as sysjson
import logging
import traceback

from sanic import Sanic
from sanic.response import json
import asyncio
import srvconf
import models.errors as errors
from utils.http_helper import json_result

app = Sanic(__name__)

from controllers.sync_system_handler import Sync

sync = Sync(app)


@app.exception(Exception)
def ignore_500s(request, exception):
    error_info = "system_error {}\n".format(type(exception))
    error_info += traceback.format_exc()
    logging.error(error_info)
    return json({"err": errors.system_error, "err_msg": error_info})


@app.listener('before_server_start')
async def setup(app, loop):
    from resources import init, get_session, get_db, get_redis_pool
    await init()

    app.db = get_db()
    app.redis_pool = get_redis_pool()
    app.session = get_session()

    await sync.init()

    loop.create_task(sync.sync())


@app.listener('after_server_stop')
async def close_service(app, loop):
    await sync.close()

    from resources import close
    await close()
