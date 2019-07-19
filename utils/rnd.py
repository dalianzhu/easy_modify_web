import base64
import os


def rnd_str():
    rnd_byte = os.urandom(6)
    b64_str = base64.urlsafe_b64encode(rnd_byte)
    return b64_str.decode()
