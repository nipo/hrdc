from ..stream import Stream

class Optimizer(Stream):
    class __metaclass__(type):
        def __init__(cls, name, bases, dct):
            type.__init__(cls, name, bases, dct)
            if hasattr(cls, "precedence"):
                Optimizer.registry.append(cls)

    registry = []

    @classmethod
    def new(cls, stream, min = 0, max = 100):
        for o in sorted(cls.registry, lambda x, y: cmp(x.precedence, y.precedence)):
            if min < o.precedence < max:
#                print o.__name__
                stream = o(stream)
        return stream
