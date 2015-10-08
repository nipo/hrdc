from ..stream import Stream

class Formatter(Stream):
    class __metaclass__(type):
        def __init__(cls, name, bases, dct):
            type.__init__(cls, name, bases, dct)
            try:
                Formatter.registry[cls.__name__.lower()] = cls
            except:
                pass

    registry = {}

    @classmethod
    def get(cls, name):
        return cls.registry[name]
