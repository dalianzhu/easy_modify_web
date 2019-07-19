from sanic.response import json

code_is_incorrect = 1
svc_is_not_found = 2
svc_name_is_invalid = 3
code_is_unsafe = 4
system_error = 5
task_finish = 6


def system_error_ret(msg=""):
    return json({"err": system_error, "err_msg": msg})


def task_finish_ret():
    return json({"err": task_finish, "err_msg": "task is finish"})
