from ..stream import item

__all__ = ["Report", "Collection", "Value", "Align", "TopLevel", "Padding", "Unit"]

Unit = item.Unit

class Base:
    def accept(self, visitor):
        raise RuntimeError("This method should have been overridden")

class Hierarchical(Base):
    def __init__(self, *members):
        self.members = list(members)

    def accept(self, visitor):
        visitor.enter(self)
        for m in self.members:
            m.accept(visitor)
        visitor.leave(self)

    def __getitem__(self, i):
        return self.members[i]

    def __iter__(self):
        return iter(self.members)

    def append(self, member):
        self.members.append(member)

    def pop(self):
        self.members.pop()

    def __len__(self):
        return len(self.members)

class Report(Hierarchical):
    def __init__(self, id, *members):
        self.id = id
        Hierarchical.__init__(self, *members)

class TopLevel(Hierarchical): pass

class Collection(Hierarchical):
    Physical = item.Collection.Physical
    Application = item.Collection.Application
    Logical = item.Collection.Logical
    Report = item.Collection.Report
    NamedArray = item.Collection.NamedArray
    UsageSwitch = item.Collection.UsageSwitch
    UsageModifier = item.Collection.UsageModifier

    def __init__(self, kind, usage, *members):
        self.kind = kind
        self.usage = usage
        Hierarchical.__init__(self, *members)

class Value(Base):
    Input = item.DataItem.Input
    Output = item.DataItem.Output
    Feature = item.DataItem.Feature

    Data = item.DataItem.Data
    Constant = item.DataItem.Constant
    Array = item.DataItem.Array
    Variable = item.DataItem.Variable
    Absolute = item.DataItem.Absolute
    Relative = item.DataItem.Relative
    NoWrap = item.DataItem.NoWrap
    Wrap = item.DataItem.Wrap
    Linear = item.DataItem.Linear
    NonLinear = item.DataItem.NonLinear
    PreferredState = item.DataItem.PreferredState
    NoPreferred = item.DataItem.NoPreferred
    NoNullPosition = item.DataItem.NoNullPosition
    NullState = item.DataItem.NullState
    NonVolatile = item.DataItem.NonVolatile
    Volatile = item.DataItem.Volatile
    BitField = item.DataItem.BitField
    BufferedBytes = item.DataItem.BufferedBytes
    
    def __init__(self, way, usage, size,
                 flags = Data | Variable | Absolute,
                 logicalMin = 1, logicalMax = None,
                 physicalMin = None, physicalMax = None,
                 namedArray = None,
                 unit = 0, unitExponent = 0,
                 designator = 0,
                 string = 0,
                 count = 1,
                 alignment = None):
        self.way = way
        self.flags = flags
        self.usage = usage
        self.size = size
        if alignment is None:
            self.alignment = min((8, self.size))
        else:
            self.alignment = alignment
        if (logicalMax == None or logicalMin == None) \
               and not namedArray \
               and not (flags & self.Constant):
            raise ValueError("Must specify either logical bounds or a named array")
        self.logicalMin = logicalMin
        self.logicalMax = logicalMax
        if not physicalMin and not physicalMax:
            self.physicalMin = logicalMin
            self.physicalMax = logicalMax
        else:
            self.physicalMin = physicalMin or 0
            self.physicalMax = physicalMax or 0
        self.namedArray = namedArray
        self.unit = unit
        self.unitExponent = unitExponent
        self.designator = designator
        self.string = string
        self.count = count

        if namedArray:
            if usage:
                self.flags = self.Variable
            else:
                self.flags = self.Data | self.Array
            self.logicalMax = len(self.namedArray) + self.logicalMin - 1

    def accept(self, visitor):
        visitor.element(self)

class Align(Value):
    def __init__(self, way, boundary, flags = Value.Constant | Value.Variable):
        Value.__init__(self, way, 0, 0, flags)
        self.boundary = boundary

class Padding(Value):
    def __init__(self, way, size):
        Value.__init__(self, way, 0, size, Value.Constant | Value.Variable)

class Visitor:
    def enter(self, element):
        pass

    def leave(self, element):
        pass

    def element(self, element):
        pass
