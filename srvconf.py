"""
配置文件全局变量都记这里吧
"""
import os

port = 8000

# redis_host = os.getenv("REDIS_HOST", "127.0.0.1")
redis_host = os.getenv("REDIS_HOST", "")  # 不用redis
redis_port = int(os.getenv("REDIS_PORT", '6379'))
redis_pwd = os.getenv("REDIS_PWD", "")
if not redis_pwd:
    redis_pwd = None


mysql_host = os.getenv("MYSQL_HOST", "")
mysql_port = int(os.getenv("MYSQL_PORT", "3306"))
mysql_user = os.getenv("MYSQL_USER", "root")
mysql_password = os.getenv("MYSQL_PWD", "123456")
database = 'db'
charset = "utf8"