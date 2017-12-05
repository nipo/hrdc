from ..util import NamedConstant

class Item:
    Main = NamedConstant("Main", 0)
    Global = NamedConstant("Global", 1)
    Local = NamedConstant("Local", 2)

    signed = False

    registry = {}

    class __metaclass__(type):
        def __init__(cls, name, bases, dct):
            type.__init__(cls, name, bases, dct)
            try:
                key = int(cls.kind), int(cls.tag)
                Item.registry[key] = cls
            except:
                pass

    @property
    def tagname(self):
        if isinstance(self.tag, NamedConstant):
            return str(self.tag)
        return self.__class__.__name__

    @classmethod
    def itemclass(cls, kind, tag):
        return cls.registry[(int(kind), int(tag))]

    @classmethod
    def parse(cls, data):
        kind = (ord(data[0]) >> 2) & 3
        tag = ord(data[0]) >> 4
        itemclass = cls.itemclass(kind, tag)
        
        size = ord(data[0]) & 0x3

        if size == 1:
            format = "<B"
        elif size == 2:
            format = "<H"
        elif size == 3:
            format = "<L"
        else:
            format = ""

        if itemclass.signed:
            format = format.lower()

        if format:
            import struct
            value = struct.unpack(format, data[1:])[0]
        else:
            value = 0

        return itemclass(value)

    def __init__(self, value):
        self.value = value or 0
        assert self.signed or int(self.value) >= 0, \
               ValueError("Unexpected value for %s: %d"
                          % (self.__class__.__name__, self.value))
        self.optionalValue = self.kind == self.Main and \
                             self.tag in (MainItem.Input, MainItem.EndCollection)

    def __str__(self):
        if int(self.value) or not self.optionalValue:
            return "%s (%s)" % (self.tagname, self.value)
        else:
            return "%s" % (self.tagname,)

    def bytes(self):
        import math
        import struct

        m = int(self.value)
        bits = int(not self.optionalValue)
        neg = self.signed and m < 0

        if neg:
            m = - m - 1

        if m:
            bits = int(math.log(m, 2)) + int(self.signed) + 1
        else:
            bits = 1 if self.value else 0

        if not bits and self.optionalValue:
            fmt = ""
            l = 0
        elif bits <= 8:
            fmt = "<B"
            l = 1
        elif bits <= 16:
            fmt = "<H"
            l = 2
        else:
            fmt = "<L"
            l = 3

        if self.signed:
            fmt = fmt.lower()

        r = chr((self.tag << 4) | (self.kind << 2) | l)
        if fmt:
            r += struct.pack(fmt, self.value)
        return r

    def __cmp__(self, other):
        if isinstance(other, Item):
            return cmp(int(self.kind), int(other.kind)) \
                   or cmp(int(self.tag), int(other.tag)) \
                   or cmp(int(self.value), int(other.value))
        if other is None:
            return 1
        return cmp(id(self), id(other))

class MainItem(Item):
    kind = Item.Main
    
    Input = NamedConstant("Input", 0x8)
    Output = NamedConstant("Output", 0x9)
    Feature = NamedConstant("Feature", 0xb)
    Collection = NamedConstant("Collection", 0xa)
    EndCollection = NamedConstant("EndCollection", 0xc)

class GlobalItem(Item):
    kind = Item.Global

    UsagePage = NamedConstant("UsagePage", 0)
    LogicalMinimum = NamedConstant("LogicalMinimum", 0x1)
    LogicalMaximum = NamedConstant("LogicalMaximum", 0x2)
    PhysicalMinimum = NamedConstant("PhysicalMinimum", 0x3)
    PhysicalMaximum = NamedConstant("PhysicalMaximum", 0x4)
    UnitExponent = NamedConstant("UnitExponent", 0x5)
    Unit = NamedConstant("Unit", 0x6)
    ReportSize = NamedConstant("ReportSize", 0x7)
    ReportID = NamedConstant("ReportID", 0x8)
    ReportCount = NamedConstant("ReportCount", 0x9)
    Push = NamedConstant("Push", 0xa)
    Pop = NamedConstant("Pop", 0xb)

class LocalItem(Item):
    kind = Item.Local

    Usage = NamedConstant("Usage", 0x0)
    UsageMinimum = NamedConstant("UsageMinimum", 0x1)
    UsageMaximum = NamedConstant("UsageMaximum", 0x2)
    DesignatorIndex = NamedConstant("DesignatorIndex", 0x3)
    DesignatorMinimum = NamedConstant("DesignatorMinimum", 0x4)
    DesignatorMaximum = NamedConstant("DesignatorMaximum", 0x5)
    StringIndex = NamedConstant("StringIndex", 0x7)
    StringMinimum = NamedConstant("StringMinimum", 0x8)
    StringMaximum = NamedConstant("StringMaximum", 0x9)
    Delimiter = NamedConstant("Delimiter", 0xa)

class DataItem(MainItem):
    Data = NamedConstant("Data", 0)
    Constant = NamedConstant("Constant", 1)
    Array = NamedConstant("Array", 0)
    Variable = NamedConstant("Variable", 2)
    Absolute = NamedConstant("Absolute", 0)
    Relative = NamedConstant("Relative", 4)
    NoWrap = NamedConstant("NoWrap", 0)
    Wrap = NamedConstant("Wrap", 8)
    Linear = NamedConstant("Linear", 0)
    NonLinear = NamedConstant("NonLinear", 16)
    PreferredState = NamedConstant("PreferredState", 0)
    NoPreferred = NamedConstant("NoPreferred", 32)
    NoNullPosition = NamedConstant("NoNullPosition", 0)
    NullState = NamedConstant("NullState", 64)
    NonVolatile = NamedConstant("NonVolatile", 0)
    Volatile = NamedConstant("Volatile", 128)
    BitField = NamedConstant("BitField", 0)
    BufferedBytes = NamedConstant("BufferedBytes", 256)

    _rev = [Constant, Variable, Relative,
            Wrap, NonLinear, NoPreferred,
            NullState, Volatile, BufferedBytes]

    def __init__(self, value):
        if not isinstance(value, NamedConstant):
            i = int(value)
            v = [r for r in self._rev if int(r) & i]
            value = NamedConstant("|".join(x.name for x in v) or "Array", i)
        MainItem.__init__(self, value)

class Input(DataItem):
    tag = MainItem.Input

class Output(DataItem):
    tag = MainItem.Output

class Feature(DataItem):
    tag = MainItem.Feature

class Collection(MainItem):
    tag = MainItem.Collection

    Physical = NamedConstant("Physical", 0)
    Application = NamedConstant("Application", 1)
    Logical = NamedConstant("Logical", 2)
    Report = NamedConstant("Report", 3)
    NamedArray = NamedConstant("NamedArray", 4)
    UsageSwitch = NamedConstant("UsageSwitch", 5)
    UsageModifier = NamedConstant("UsageModifier", 6)

    _rev = [Physical, Application, Logical, Report, NamedArray, UsageSwitch, UsageModifier]

    def __init__(self, value):
        if not isinstance(value, NamedConstant) and int(value) < len(self._rev):
            value = self._rev[int(value)]
        MainItem.__init__(self, value)

class EndCollection(MainItem):
    tag = MainItem.EndCollection

    def __init__(self, val = 0):
        assert val == 0
        MainItem.__init__(self, 0)

class UsagePage(GlobalItem):
    tag = GlobalItem.UsagePage

class LogicalMinimum(GlobalItem):
    signed = True
    tag = GlobalItem.LogicalMinimum

class LogicalMaximum(GlobalItem):
    signed = True
    tag = GlobalItem.LogicalMaximum

class PhysicalMinimum(GlobalItem):
    signed = True
    tag = GlobalItem.PhysicalMinimum

class PhysicalMaximum(GlobalItem):
    signed = True
    tag = GlobalItem.PhysicalMaximum

class UnitExponent(GlobalItem):
    signed = True
    tag = GlobalItem.UnitExponent

def _unit_nibble(val, pos):
    assert -8 <= val <= 7
    if val < 0:
        val += 0x10
    return val << (pos * 4)

class Unit(GlobalItem):
    tag = GlobalItem.Unit

    SILinear = NamedConstant("SILinear", 1)
    SIRotation = NamedConstant("SIRotation", 2)
    EnglishLinear = NamedConstant("EnglishLinear", 3)
    EnglishRotation = NamedConstant("EnglishRotation", 4)

    def length(x):
        return _unit_nibble(x, 1)

    def mass(x):
        return _unit_nibble(x, 2)

    def time(x):
        return _unit_nibble(x, 3)

    def temperature(x):
        return _unit_nibble(x, 4)

    def current(x):
        return _unit_nibble(x, 5)

    def luminousintensity(x):
        return _unit_nibble(x, 6)

    Centimeter = NamedConstant("Centimeter", SILinear | length(1))
    Radian = NamedConstant("Radian", SIRotation | length(1))
    Inch = NamedConstant("Inch", EnglishLinear | length(1))
    Degree = NamedConstant("Degree", EnglishRotation | length(1))
    Gram = NamedConstant("Gram", SILinear | mass(1))
    Slug = NamedConstant("Slug", EnglishLinear | mass(1))
    Second = NamedConstant("Second", time(1))
    Kelvin = NamedConstant("Kelvin", SILinear | temperature(1))
    Fahrenheit = NamedConstant("Fahrenheit", EnglishLinear | temperature(1))
    Ampere = NamedConstant("Ampere", current(1))
    Candela = NamedConstant("Candela", luminousintensity(1))
    CmPerSec = NamedConstant("Velocity", SILinear | time(-1) | length(1))
    Momentum = NamedConstant("Momentum", SILinear | time(-1) | length(1) | mass(1))
    G = NamedConstant("G", SILinear | time(-2) | length(1))
    Newton = NamedConstant("Newton", SILinear | time(-2) | length(1) | mass(1))
    Joule = NamedConstant("Joule", SILinear | time(-2) | length(2) | mass(1))
    Volt = NamedConstant("Volt", SILinear | time(-3) | length(2) | mass(1) | current(-1))

    _usual_units = {
        int(Centimeter): Centimeter,
        int(Radian): Radian,
        int(Inch): Inch,
        int(Degree): Degree,
        int(Gram): Gram,
        int(Slug): Slug,
        int(Second): Second,
        int(Kelvin): Kelvin,
        int(Fahrenheit): Fahrenheit,
        int(Ampere): Ampere,
        int(Candela): Candela,
        int(CmPerSec): CmPerSec,
        int(Momentum): Momentum,
        int(G): G,
        int(Newton): Newton,
        int(Joule): Joule,
        int(Volt): Volt,
        }

    length = staticmethod(length)
    mass = staticmethod(mass)
    time = staticmethod(time)
    temperature = staticmethod(temperature)
    current = staticmethod(current)
    luminousintensity = staticmethod(luminousintensity)

    def __init__(self, value):
#        if value and value & 0xf == 0:
#            value = value | self.SILinear
        value = self._usual_units.get(value, value)
        GlobalItem.__init__(self, value)

class ReportSize(GlobalItem):
    tag = GlobalItem.ReportSize

class ReportID(GlobalItem):
    tag = GlobalItem.ReportID

class ReportCount(GlobalItem):
    tag = GlobalItem.ReportCount

class Push(GlobalItem):
    tag = GlobalItem.Push

    def __init__(self, val = 0):
        assert val == 0
        GlobalItem.__init__(self, 0)

class Pop(GlobalItem):
    tag = GlobalItem.Pop

    def __init__(self, val = 0):
        assert val == 0
        GlobalItem.__init__(self, 0)

class Usage(LocalItem):
    tag = LocalItem.Usage

    def __init__(self, value):
        from ..usage.usage import Usage as _Usage
        if not isinstance(value, _Usage):
            value = _Usage.lookup(value)
        LocalItem.__init__(self, value)

class UsageMinimum(LocalItem):
    tag = LocalItem.UsageMinimum

    def __init__(self, value):
        from ..usage.usage import Usage as _Usage
        if not isinstance(value, _Usage):
            value = _Usage.lookup(value)
        LocalItem.__init__(self, value)

class UsageMaximum(LocalItem):
    tag = LocalItem.UsageMaximum

    def __init__(self, value):
        from ..usage.usage import Usage as _Usage
        if not isinstance(value, _Usage):
            value = _Usage.lookup(value)
        LocalItem.__init__(self, value)

class DesignatorIndex(LocalItem):
    tag = LocalItem.DesignatorIndex

class DesignatorMinimum(LocalItem):
    tag = LocalItem.DesignatorMinimum

class DesignatorMaximum(LocalItem):
    tag = LocalItem.DesignatorMaximum

class StringIndex(LocalItem):
    tag = LocalItem.StringIndex

class StringMinimum(LocalItem):
    tag = LocalItem.StringMinimum

class StringMaximum(LocalItem):
    tag = LocalItem.StringMaximum

class Delimiter(LocalItem):
    tag = LocalItem.Delimiter
