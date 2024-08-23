import os
from string import Template


class SQLProvider:
    def __init__(self, filepath: str):
        self._scripts = {}
        for file in os.listdir(filepath):
            sql = open(f'{filepath}/{file}').read()
            self._scripts[file] = Template(sql)

    def get(self, filename: str, **kwargs):
        sql = self._scripts[filename].substitute(**kwargs)
        return sql
