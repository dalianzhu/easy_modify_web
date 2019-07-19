import os
import codecs
import json

with codecs.open(os.getcwd() + "/sys_handlers.json") as f:
    system_handler_list = json.loads(f.read())

will_close = True