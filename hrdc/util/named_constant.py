
class NamedConstant:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __int__(self):
        return self.value

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return int(self) < int(other)

    def __eq__(self, other):
        return int(self) == int(other)

    def __hash__(self):
        return hash(int(self))

    def __add__(self, other):
        if isinstance(other, (NamedConstant, int)):
            return self.value + int(other)
        raise NotImplemented()

    def __invert__(self):
        return ~int(self)

    def __mul__(self, other):
        if isinstance(other, (NamedConstant, int)):
            return self.value * int(other)
        raise NotImplemented()

    def __and__(self, other):
        if isinstance(other, (NamedConstant, int)):
            return self.value & int(other)
        raise NotImplemented()

    def __rand__(self, other):
        if isinstance(other, (NamedConstant, int)):
            return self.value & int(other)
        raise NotImplemented()

    def __lshift__(self, other):
        if isinstance(other, (NamedConstant, int)):
            return self.value << int(other)
        raise NotImplemented()

    def __rshift__(self, other):
        if isinstance(other, (NamedConstant, int)):
            return self.value >> int(other)
        raise NotImplemented()

    def __or__(self, other):
        if isinstance(other, (NamedConstant, int)):
            return self.value | int(other)
        raise NotImplemented()

    def __ror__(self, other):
        if isinstance(other, (NamedConstant, int)):
            return self.value | int(other)
        raise NotImplemented()


