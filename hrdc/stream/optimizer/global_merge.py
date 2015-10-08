from base import Optimizer

class GlobalMerge(Optimizer):
    precedence = 40

    def __init__(self, stream):
        from ..item import Item, GlobalItem, Unit, UnitExponent, \
             PhysicalMinimum, PhysicalMaximum, \
             LogicalMinimum, LogicalMaximum

        self.stream = stream
        self.locals = {}
        self.globals = {
            GlobalItem.Unit: Unit(0),
            GlobalItem.UnitExponent: UnitExponent(0),
            GlobalItem.LogicalMinimum: LogicalMinimum(0),
            GlobalItem.LogicalMaximum: LogicalMaximum(0),
            GlobalItem.PhysicalMinimum: PhysicalMinimum(0),
            GlobalItem.PhysicalMaximum: PhysicalMaximum(0),
            }

    def append(self, item):
        from ..item import Item, GlobalItem

        if item.kind == Item.Global:
            if self.globals.get(item.tag, None) != item \
                   or item.tag == GlobalItem.Push \
                   or item.tag == GlobalItem.Pop:
                self.stream.append(item)
            self.globals[item.tag] = item

        elif item.kind == Item.Local:
            self.stream.append(item)

        else:
            self.locals = {}
            self.stream.append(item)
