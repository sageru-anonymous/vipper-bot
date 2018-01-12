"""Provides a clean "API" for regular expression based bot responses. These
are used in handlers.py.
"""
# The dispatch table maps regular expressions to functions that accept a
# `client` argument and a `message` argument. Read access to this table is
# permitted by any module but write access should only be done within this
# module.
DISPATCH_TABLE = {}


class bot_response(object):
    """Decorator for regular expression based bot responses."""
    def __init__(self, regexp):
        self.regexp = regexp

    def __call__(self, handler):
        DISPATCH_TABLE[self.regexp] = handler
        return handler
