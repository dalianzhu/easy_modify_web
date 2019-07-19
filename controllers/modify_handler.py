import types
import logging


def add_handler(app, name, func, code, web_path):
    md = types.ModuleType(name)
    exec(code, md.__dict__)

    http_handler = getattr(md, func)

    rm_handler(app, web_path)
    logging.info("add_handler {}".format(web_path))

    app.add_route(http_handler, web_path, methods={"GET", "POST"}, name=name)


def rm_handler(app, web_path):
    logging.info("rm_handler {}".format(web_path))

    try:
        app.remove_route(web_path)
    except:
        pass

    try:
        app.remove_route(web_path+"/")
    except:
        pass
