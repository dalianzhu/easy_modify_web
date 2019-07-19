import os
import codecs
import json
import datetime

with codecs.open(os.getcwd() + "/sys_handlers.json", "r") as f:
    content = json.loads(f.read())

for name in content:
    handler = content[name]
    handler["update_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with codecs.open(os.getcwd() + "/sys_handlers.json", "w") as f:
    f.write(json.dumps(content))