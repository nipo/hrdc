from ..stream import Stream

class _FormatterMeta(type):
    def __init__(cls, name, bases, dct):
        type.__init__(cls, name, bases, dct)
        try:
            Formatter.registry[cls.__name__.lower()] = cls
        except:
            pass

class Formatter(Stream, metaclass = _FormatterMeta):

    registry = {}

    @classmethod
    def get(cls, name):
        return cls.registry[name]
