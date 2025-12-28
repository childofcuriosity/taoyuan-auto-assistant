import json
import subprocess

from src.adb_utils import run_touchlink


class TouchLink(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._proc = run_touchlink('touchlink.apk', '/data/local/tmp/touchlink.apk')

    def _emit(self, data):
        data = {
            'action': 'input',
            'params': {
                'inputs': data
            }
        }

        self._proc.stdin.write(json.dumps(data).encode() + b'\n')
        self._proc.stdin.flush()
        self._proc.stdout.readline()

    def touch(self, x, y):
        self._emit([{'action': 'touch', 'args': [x, y]}])

    def swipe(self, x1, y1, x2, y2):
        self._emit([{'action': 'swipe', 'args': [x1, y1, x2, y2]}])

    def swipe_path(self, points):
        self._emit([{'action': 'swipe', 'args': points}])

    def custom(self, data):
        self._emit(data)