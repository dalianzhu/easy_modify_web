import json

import requests

code = """
import logging
from sanic.response import json


async def subscribe(request):
    # {
    #   "data": {} // 推送的数据,
    #   "timestamp": 1554190910,
    #   "sub_id": 111, // 订阅ID
    # }
    # 接口的response必须满足：
    # - response:
    # {
    #   "code": 200, // 200为正常，其余值为不正常
    #   "msg": "" // 传给服务器的信息
    # }
    return json({
        "code": 200,  # 200为正常，其余值为不正常
        "msg": ""  # 传给服务器的信息
    })

"""


def test_add(host):
    url = "{}/{}".format(host, "add")
    data = {
        "name": "subscribe",
        "code": code,
        "web_path": "/subscribe",
        "admin_pwd": "123456"
    }
    ret = requests.post(url, json.dumps(data))
    print(ret.text)
