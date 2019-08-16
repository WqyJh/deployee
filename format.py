import re
import inspect


def format(template: str) -> str:
    calframe = inspect.currentframe().f_back
    d = calframe.f_globals.copy()
    d.update(calframe.f_locals)

    keys = re.findall(r'{(\w+?)}', template)
    args = {k: d.get(k, '') for k in keys}
    return template.format(**args)
