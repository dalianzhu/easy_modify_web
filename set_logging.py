import logging
import logging.handlers
import os
import socket


def set_logging():
    # 获取本机电脑名
    myname = socket.getfqdn(socket.gethostname())
    # 获取本机ip
    myaddr = socket.gethostbyname(myname)

    fmt = '%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'

    logger = logging.getLogger()

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(fmt, datefmt))

    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename='./logs/{}.log'.format(myaddr),
        when="midnight",
        backupCount=5)
    file_handler.setFormatter(logging.Formatter(fmt, datefmt))

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(os.getenv("logLevel", "DEBUG").upper())
