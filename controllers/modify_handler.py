import logging
import traceback
import types

import models.db
from models.global_items import system_handler


def add_handler(app, func_item: models.db.FuncItem):
    logging.debug("add handler func_item:{}".format(func_item))
    if not func_item:
        logging.error(traceback.format_exc())
        raise Exception("func item is none")
    try:
        md = types.ModuleType(func_item.name)
        exec(func_item.code, md.__dict__)

        http_handler = getattr(md, func_item.name)

        rm_handler(app, func_item.name)
        logging.info("add_handler {}".format(func_item.web_path))

        app.add_route(http_handler, func_item.web_path, methods={
            "GET", "POST"}, name=func_item.name)
        system_handler[func_item.name] = func_item

    except:
        logging.error(traceback.format_exc())


def rm_handler(app, name):
    func_item = system_handler.get(name)
    if not func_item:
        logging.error("cannot find {}".format(name))
        return

    logging.info("rm_handler {}".format(func_item.web_path))
    try:
        app.remove_route(func_item.web_path)
    except:
        pass

    try:
        app.remove_route(func_item.web_path + "/")
    except:
        pass
