import re
import inspect


def format(template: str) -> str:
    calframe = inspect.currentframe().f_back
    d = calframe.f_globals.copy()
    d.update(calframe.f_locals)

    keys = re.findall(r'{([\w.]+?)}', template)

    def _eval(k, d):
        if '.' in k:
            key, path = k.split('.', maxsplit=1)
            obj = d.get(key, None) or ''
            return key, obj
        return k, d.get(k, '')

    args = dict(_eval(k, d) for k in keys)
    return template.format(**args)
