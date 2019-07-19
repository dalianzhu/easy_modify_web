from models.global_items import system_handler_list
from resources import redis_set, redis_get
import os
import codecs
import asyncio
from controllers.modify_handler import add_handler, rm_handler
import logging


class Sync(object):
    def __init__(self, app):
        self.app = app
        self._is_close = False
        self._running = True

    async def close(self):
        self._running = False
        while 1:
            if self._is_close:
                return
            else:
                await asyncio.sleep(1)

    async def init(self):
        # 把system handler更新到db
        db_handler_list = await redis_get("db_handler_list")
        if not db_handler_list:
            db_handler_list = {}

        db_change = False
        for name in system_handler_list:
            handler = system_handler_list[name]
            file_path = handler['file_path']
            with codecs.open("{}/{}".format(os.getcwd(), file_path), "r") as f:
                handler['code'] = f.read()

            add_handler(self.app,
                        handler['name'],
                        handler['func'],
                        handler['code'],
                        handler['web_path'])

            if name not in db_handler_list:
                # 说明redis中还没有这些东西
                db_handler_list[name] = handler
                db_change = True
        if db_change:
            logging.debug("db is change")
            await redis_set("db_handler_list", 0, db_handler_list)

    async def sync(self):
        """
        handler_info
        {
            "name": "add_handler",
            "file_path": "handlers/add_handler.py",
            "func": "add_handler",
            "web_path": "/add",
            "code": "xxx",
            "update_time": "2019-07-19 00:00:00"
        },
        """
        while self._running:
            await asyncio.sleep(1)
            db_handler_list = await redis_get("db_handler_list")
            if not db_handler_list:
                db_handler_list = {}

            # logging.debug("system_handler_list {}".format(system_handler_list))

            # 把db_handler更新到system handler
            for name in db_handler_list:
                handler = db_handler_list[name]
                if name not in system_handler_list:
                    logging.debug("sync will add handler {}".format(name))
                    system_handler_list[name] = handler
                    add_handler(self.app,
                                handler['name'],
                                handler['func'],
                                handler['code'],
                                handler['web_path'],
                                )

                db_update_time = handler['update_time']
                sys_update_time = system_handler_list[name]['update_time']

                if db_update_time > sys_update_time:
                    # 数据库中的函数更新，使用数据库的数据更新系统
                    logging.debug("sync will add handler {}".format(name))

                    system_handler_list[name] = handler
                    add_handler(self.app,
                                handler['name'],
                                handler['func'],
                                handler['code'],
                                handler['web_path'])

            will_rm = []
            for name in system_handler_list:
                handler = system_handler_list[name]
                if name not in db_handler_list:
                    logging.debug("sync will rm handler {}".format(name))
                    will_rm.append(name)
                    rm_handler(self.app, handler['web_path'])

            for name in will_rm:
                del system_handler_list[name]

        self._is_close = True
