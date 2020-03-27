from sanic.response import html

import models.db
import models.errors
import utils.time
from controllers.wraps import admin_pwd
from utils.http_helper import get_req_key
import types
from sanic import Sanic
import traceback
from models.errors import system_error_ret
from utils.http_helper import get_req_key


@admin_pwd
async def get_page(request):
    name = get_req_key(request, "name")
    pwd = get_req_key(request, "admin_pwd")

    if not name:
        func = models.db.FuncItem()
    else:
        db = models.db.FileDB()
        func = db.list().get(name)
        if not func:
            return system_error_ret("{} is not exists".format(name))

    content = """
<html>
    <body>
        <h1>编辑</h1>
        <form method="post" action="/add">
            函数名：<br>
            <input type="text" name="name" value="@#NAME"/><br>
            web path：<br>
            <input type="text" name="web_path" value="@#WEBPATH"/>
            <input type="hidden" name="admin_pwd" value="@#PWD"/>
            代码:<br> 
            <textarea cols="50" rows="10" name="code">@#CODE</textarea>
            <br>
            <input type="submit" value="提交" />
        </form> 
    </body>
</html>
"""
    content = content.replace("@#NAME", func.name). \
        replace("@#CODE", func.code). \
        replace("@#WEBPATH", func.web_path). \
        replace("@#PWD", pwd)
    return html(content)
