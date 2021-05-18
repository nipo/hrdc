from .. import util as _util

class Usage(_util.NamedConstant):
    reverse = dict()

    def __init__(self, name, value, *kinds, **opts):
        register = opts.get('register', True)
        _util.NamedConstant.__init__(self, name, value)
        self.kinds = set(kinds)
        if register:
            self.reverse[int(value)] = self

    @classmethod
    def page(cls, no):
        no = int(no)
        name = cls.pageName.get(no, str(no))
        return _util.NamedConstant(name, no)

    @classmethod
    def inpage(cls, page, no):
        u = cls.lookup((int(page) << 16) | int(no))
        sp, su = u.split()
        return su

    pageName = {
        0x1: "GenericDesktop",
        0x2: "Simulation",
        0x3: "VR",
        0x5: "Game",
        0x6: "Device",
        0x7: "Keyboard",
        0x8: "Led",
        0x9: "Button",
        0xa: "Ordinal",
        0xb: "TelephonyDevice",
        0xc: "Consumer",
        0xd: "Digitizers",
        0xf: "PID",
        0x20: "Sensors",
        0x90: "Camera",
        0xff00: "Arcade",
    }

    @classmethod
    def lookup(cls, value):
        if isinstance(value, Usage):
            return value
        if isinstance(value, _util.NamedConstant):
            return Usage(value.name, int(value.value), register = False)
        if int(value) >> 16:
            try:
                return cls.reverse[int(value)]
            except:
                pass
        return cls(hex(int(value)), int(value), register = False)

    def split(self):
        try:
            p, u = self.name.split(".", 1)
            return (
                _util.NamedConstant(p, self.value >> 16),
                _util.NamedConstant(u, self.value & 0xffff),
                )
        except:
            u = int(self.value) & 0xffff
            return self.page(int(self.value) >> 16), _util.NamedConstant(str(u), u)

class UsageRange:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def __str__(self):
        return "UsageRange(%s, %s)" % (self.min, self.max)

    def __len__(self):
        return int(self.max) - int(self.min) + 1

    def __getitem__(self, no):
        return Usage.lookup(int(self.min) + no)

    def __iter__(self):
        for i in range(int(self.min), int(self.max) + 1):
            yield Usage.lookup(i)

    @classmethod
    def from_array(cls, arr):
        if len(arr) < 2:
            raise ValueError("Cannot create range from array with less than 2 elements")
        for i, j in zip(arr, arr[1:]):
            if int(i) + 1 != int(j):
                raise ValueError("Noncontiguous values")
        return cls(arr[0], arr[-1])

class UsageType:
    def __init__(self, name):
        self.name = name

    def test(self, usage):
        usage = Usage.lookup(usage)
        if isinstance(usage, Usage):
            return self in usage.kinds
        return False

CA = UsageType("Collection Application")
CL = UsageType("Collection Logical")
CP = UsageType("Collection Physical")
RTC = UsageType("Re-Trigger Control")
LC = UsageType("Linear Control")
MC = UsageType("Momentary Control")
OSC = UsageType("One Shot Control")
Sel = UsageType("Selector")
SV = UsageType("Static Value")
SF = UsageType("Static Flag")
DF = UsageType("Dynamic Flag")
DV = UsageType("Dynamic Value")
NAry = UsageType("Named Array")
US = UsageType("Usage Switch")
UM = UsageType("Usage Modifier")
OOC = UsageType("On/Off Control")
