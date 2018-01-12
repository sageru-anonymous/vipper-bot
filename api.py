"""Provides a clean "API" for regular expression based bot responses. These
are used in handlers.py.
"""
# The dispatch table maps regular expressions and functions that accept a
# `client` argument and a `message` argument. Read access to this table is
# permitted by any module but write access should only be done within this
# module.
DISPATCH_TABLE = []


class bot_response(object):
    """Decorator for regular expression based bot responses."""
    def __init__(self, regexp, *args):
        self.regexp = regexp
        self.args = args

    def __call__(self, handler):
        DISPATCH_TABLE.append((self.regexp, self.args, handler))
        return handler
