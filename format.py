import re
import inspect


def format(template: str) -> str:
    calframe = inspect.currentframe().f_back
    d = calframe.f_globals.copy()
    d.update(calframe.f_locals)

    keys = re.findall(r'{([\w.]+?)}', template)

    def _eval(k, d):
        if '.' in k:
            ret = ''
            key, path = k.split('.', maxsplit=1)
            obj = d.get(key, None) or ''
            # if obj:
            #     ret = operator.attrgetter(path)(obj)
            #     ret = ret if ret else ''
            return key, obj
        return k, d.get(k, '')

    args = dict(_eval(k, d) for k in keys)
    print(args, template)
    return template.format(**args)
