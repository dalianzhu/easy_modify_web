import json
import os
from typing import Dict


class FuncItem(object):
    def __init__(self):
        self.name = ""
        self.file_path = ""
        self.type = ""
        self.web_path = ""
        self.last_update = ""
        self._code = ""

    @property
    def code(self) -> str:
        if self._code:
            return self._code
        if self.file_path:
            with open("{}/{}".format(os.getcwd(), self.file_path), "r") as f:
                self._code = f.read()
                return self._code
        return ""

    @code.setter
    def code(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._code = value


class DBInterface(object):
    def __init__(self):
        pass

    def get(self, name: str) -> FuncItem:
        pass

    def set(self, name: str, val: FuncItem):
        pass

    def list(self) -> Dict[str, FuncItem]:
        pass

    def rm(self, name: str):
        pass


class FileDB(DBInterface):
    def __init__(self):
        self.db_file = "{}/sys_handlers.json".format(os.getcwd())

    def _getfile(self) -> dict:
        with open(self.db_file, mode="r", encoding="utf8") as f:
            content = f.read()
            js_content = json.loads(content)
            return js_content

    def _save_file(self, content: str):
        with open(self.db_file, mode="w", encoding="utf8") as f:
            f.write(content)

    def get(self, name: str) -> FuncItem:
        js_content = self._getfile()
        jsval = js_content.get(name)
        if jsval:
            tp = FuncItem()
            tp.name = name
            tp.file_path = jsval.get("file_path", "")
            tp.type = jsval.get("type", "")
            tp.web_path = jsval.get("web_path", "")
            tp.last_update = jsval.get("last_update", "")
            tp.code = jsval.get("code", "")
            return tp
        return None

    def set(self, name: str, val: FuncItem):
        js_content = self._getfile()
        js_content[name] = {
            "file_path": val.file_path,
            "type": val.type,
            "web_path": val.web_path,
            "last_update": val.last_update,
            "code": val.code,
        }
        content = json.dumps(js_content)
        self._save_file(content)

    def rm(self, name: str):
        js_content = self._getfile()
        if name in js_content:
            del js_content[name]
            content = json.dumps(js_content)
            self._save_file(content)

    def list(self) -> Dict[str, FuncItem]:
        js_content = self._getfile()
        ret = {}
        for func_name in js_content:
            jsval = js_content[func_name]
            tp = FuncItem()
            tp.name = func_name
            tp.file_path = jsval.get("file_path", "")
            tp.type = jsval.get("type", "")
            tp.web_path = jsval.get("web_path", "")
            tp.last_update = jsval.get("last_update", "")
            tp.code = jsval.get("code", "")
            ret[func_name] = tp

        return ret
