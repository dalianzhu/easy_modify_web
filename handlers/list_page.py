from sanic.response import html

import models.db
import models.errors
import utils.time
from controllers.wraps import admin_pwd
from utils.http_helper import get_req_key
import types
from sanic import Sanic
import traceback


@admin_pwd
async def list_page(request):
    content = """
<html>
    <body>
        <a target="view_window" href='/get_page?admin_pwd=@#PWD'>创建新函数</a> 
        <h1>列表</h1>
        @#LIST
    </body>
</html>
"""
    pwd = get_req_key(request, "admin_pwd")
    db = models.db.FileDB()
    func_list = db.list()
    show_arr = []
    for name in func_list:
        func = func_list[name]
        if func.type == "system":
            continue
        show_arr.append("""<li>
                        <a target="view_window" width='70%' href='/get_page?name={}&admin_pwd={}'>{}</a>
                        <a target="view_window" href='/rm?name={}&admin_pwd={}'>删除</a>
                        </li>""".format(func.name, pwd, func.name,
                                        func.name, pwd))

    show_content = "\n".join(show_arr)
    content = content. \
        replace("@#LIST", show_content). \
        replace("@#PWD", pwd)

    return html(content)
