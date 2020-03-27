from models.global_items import get_system_handler
import models.db
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
        db = models.db.FileDB()
        db_handler_list = db.list()

        for name in db_handler_list:
            func_item = db_handler_list[name]
            add_handler(self.app, func_item)

    async def sync(self):
        """
        handler_info
        "rm_handler": {
            "type": "system",
            "file_path": "handlers/rm_handler.py",
            "func": "rm_handler",
            "web_path": "/rm",
            "last_update": "2019-07-19 14:43:35",
            "code": ""
        }
        """
        while self._running:
            logging.info("sync run")
            db = models.db.FileDB()
            db_handler_list = db.list()
            system_handler = get_system_handler()

            # 把db_handler更新到system handler
            for name in db_handler_list:
                func_item = db_handler_list[name]
                if name not in system_handler:
                    logging.debug("sync will add handler {}".format(name))
                    add_handler(self.app, func_item)
                else:
                    sys_func_item = system_handler[name]
                    db_update_time = func_item.last_update
                    sys_update_time = sys_func_item.last_update

                    if db_update_time > sys_update_time:
                        # 数据库中的函数更新，使用数据库的数据更新系统
                        logging.debug("sync will add handler {}".format(name))
                        add_handler(self.app, func_item)

            will_rm = []
            for name in system_handler:
                if name not in db_handler_list:
                    logging.debug("sync will rm handler {}".format(name))
                    will_rm.append(name)
            for name in will_rm:
                rm_handler(self.app, name)

            await asyncio.sleep(15)
        self._is_close = True
