import os
import codecs
import json
import models.db
from typing import Dict

system_handler = {}


def get_system_handler() -> Dict[str, models.db.FuncItem]:
    return system_handler


will_close = True
