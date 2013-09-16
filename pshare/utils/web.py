import flask
import json as real_json

VIEW_DEFAULTS = dict()

def view(name):
    if not name.endswith('.html'):
        name = name + '.html'

    def fn(f):
        def handler(*args, **kwargs):
            res = f(*args, **kwargs)

            if res and not isinstance(res, (dict)):
                return res

            data = VIEW_DEFAULTS.copy()
            if res:
                data.update(res)

            return flask.render_template(name, **data)

        handler.__name__ = f.__name__
        return handler
    return fn

def json(pretty_print = False):
    def fn(f):
        def handler(*args, **kwargs):
            res = f(*args, **kwargs)

            if res and not isinstance(res, (dict, list, set)):
                return res

            if pretty_print:
                return real_json.dumps(res, sort_keys = True, indent = 4, separators = (',', ': '))
            else:
                return real_json.dumps(res)

        handler.__name__ = f.__name__
        return handler
    return fn
