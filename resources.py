import asyncio
import logging
import pickle

import aiohttp
import aiomysql
import aioredis
import boto3

import srvconf

handler_lock = asyncio.Lock()


class _Resources(object):
    def __init__(self):
        self._inner_redis_pool = None
        self._inner_db = None
        self._inner_session = None
        self._inner_cos = None


_res = _Resources()


async def init():
    loop = asyncio.get_event_loop()
    # 初始化redis
    redis_host = srvconf.redis_host
    redis_port = srvconf.redis_port

    if redis_host != "":
        logging.info("redis {} {} {}".format(srvconf.redis_host,
                                             srvconf.redis_port,
                                             srvconf.redis_pwd))
        _res._inner_redis_pool = await aioredis.create_redis_pool(
            (redis_host, redis_port),
            password=srvconf.redis_pwd,
            minsize=5,
            maxsize=100,
            loop=loop
        )

    # 初始化mysql
    mysql_host = srvconf.mysql_host
    if mysql_host != "":
        _res._inner_db = await aiomysql.create_pool(host=srvconf.mysql_host,
                                                    port=srvconf.mysql_port,
                                                    user=srvconf.mysql_user,
                                                    password=srvconf.mysql_password,
                                                    db=srvconf.database,
                                                    loop=loop,
                                                    charset=srvconf.charset,
                                                    autocommit=True)

    # 初始化session
    _res._inner_session = aiohttp.ClientSession(loop=loop)
    return


async def close():
    if _res._inner_session:
        await _res._inner_session.close()

    if _res._inner_db:
        _res._inner_db.close()
        await _res._inner_db.wait_closed()

    if _res._inner_redis_pool:
        _res._inner_redis_pool.close()
        await _res._inner_redis_pool.wait_closed()


def get_redis_pool():
    return _res._inner_redis_pool


def get_db():
    return _res._inner_db


def get_session():
    return _res._inner_session


async def redis_set(key: str, timeout: int, val: object):
    val_bytes = pickle.dumps(val, protocol=pickle.HIGHEST_PROTOCOL)
    if timeout == 0:
        await get_redis_pool().set(key, val_bytes)
    else:
        await get_redis_pool().setex(key, timeout, val_bytes)


async def redis_get(key: str) -> object:
    val = await get_redis_pool().get(key)
    if not val:
        return None

    val_bytes = pickle.loads(val)
    return val_bytes
