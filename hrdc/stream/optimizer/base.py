from ..stream import Stream

class _OptimizerMeta(type):
    def __init__(cls, name, bases, dct):
        type.__init__(cls, name, bases, dct)
        if hasattr(cls, "precedence"):
            Optimizer.registry.append(cls)

class Optimizer(Stream, metaclass = _OptimizerMeta):
    registry = []

    @classmethod
    def new(cls, stream, min = 0, max = 100):
        for o in sorted(cls.registry,
                        key = lambda x: x.precedence):
            if min < o.precedence < max:
#                print o.__name__
                stream = o(stream)
        return stream
