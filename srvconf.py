"""
配置文件全局变量都记这里吧
"""
import os

port = 8000
admin_pwd = os.getenv("EASYADMIN_PWD", "123456")
