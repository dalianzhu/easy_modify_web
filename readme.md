## 简介
这个网站可以自己修改handlers，修改的数据放在了文件中。这样，就可以通过http请求简单的增加删除handler了，也就是说，它可以热更新。用来做一些脚本的请求管理还挺方便的

## 添加handler
python:示例
```
import json
import requests

host = "http://localhost:8000"

code = """
import logging
from sanic.response import json
from utils.http_helper import get_req_key

async def test_hello(request):
    name = get_req_key(request, "name", "")
    ret = {"msg": name}
    return json(ret)
"""

url = "{}/{}".format(host, "add")
data = {
    "name": "test_hello", # 必须和入口handler名称一样
    "code": code,
    "web_path": "/hello",
    "admin_pwd": "123456" # 环境变量 EASYADMIN_PWD，默认 123456
}
ret = requests.post(url, json.dumps(data))
print(ret.text)
```
此时，访问`curl http://localhost:8000/hello?name=yzh`，将返回:
```bash
{"msg":"yzh"}
```

## 删除handler

```
url = "{}/{}".format(host, "rm")
data = {
    "name": "test_hello",
}
ret = requests.post(url, json.dumps(data))
print(ret.text)
```
此时，`http://localhost:8000/hello`已被删除

## 系统handler
系统handler会在初始化的时候被添加到框架中成为一个handler，系统handler的信息记录在sys_handlers.json中。
系统handler可以指定路径，用来作为代码载入的依据。

如果handler的update_time大于内存中记录的时间，则意味着系统handler需要被修改

### 修改(新建)系统handler

- 首先，在`/handlers`修改（新建）代码
- 查看`sys_handlers.json`文件中，是否登记了这个handler，如果没有则手工按规定录入
- 运行`python3 update_sys_handlers.py`，更新`sys_handlers.json`中的update_time字段为当前时间
- 重启程序 `python3 run.py`