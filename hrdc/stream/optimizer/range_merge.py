from .base import Optimizer

class RangeMerge(Optimizer):
    def __init__(self, stream, lookup, min, max):
        self.stream = stream
        self.lookup = lookup
        self.min = min
        self.max = max

        self.merging = True
        self.minValue = None
        self.maxValue = None
        self.pending = []
        self.main = None

    def flush(self):
        from ..item import Item, LocalItem

        if self.minValue and self.maxValue and self.merging:
            self.pending = [x for x in self.pending if x.kind != Item.Local or x.tag not in (self.lookup, self.min, self.max)]

            if self.minValue == self.maxValue:
                self.pending.append(Item.itemclass(Item.Local, self.lookup)(self.minValue))
            elif int(self.maxValue) - int(self.minValue) > 1:
                self.pending.append(Item.itemclass(Item.Local, self.min)(self.minValue))
                self.pending.append(Item.itemclass(Item.Local, self.max)(self.maxValue))
            else:
                self.pending.append(Item.itemclass(Item.Local, self.lookup)(self.minValue))
                self.pending.append(Item.itemclass(Item.Local, self.lookup)(self.maxValue))

        for i in self.pending:
            self.stream.append(i)
        self.pending = []

        self.merging = True
        self.minValue = None
        self.maxValue = None
        self.main = None

    def __del__(self):
        self.flush()

    def append(self, item):
        from ..item import Item, LocalItem

        if self.merging and item.kind == Item.Local:
            if item.tag in (self.min, self.max):
                self.merging = False
                
            elif item.tag == self.lookup:
                if self.maxValue is None:
                    self.maxValue = item.value
                    self.minValue = item.value
                elif int(item.value) == int(self.maxValue) + 1:
                    self.maxValue = item.value
                else:
                    self.merging = False

        if item.kind == Item.Main:
            self.flush()

        self.pending.append(item)

class DesignatorMerge(RangeMerge):
    precedence = 30

    def __init__(self, stream):
        from ..item import LocalItem
        RangeMerge.__init__(self, stream, LocalItem.DesignatorIndex, LocalItem.DesignatorMinimum, LocalItem.DesignatorMaximum)

class StringMerge(RangeMerge):
    precedence = 35

    def __init__(self, stream):
        from ..item import LocalItem
        RangeMerge.__init__(self, stream, LocalItem.StringIndex, LocalItem.StringMinimum, LocalItem.StringMaximum)

class UsageMerge(RangeMerge):
    precedence = 20

    def __init__(self, stream):
        from ..item import LocalItem
        RangeMerge.__init__(self, stream, LocalItem.Usage, LocalItem.UsageMinimum, LocalItem.UsageMaximum)
