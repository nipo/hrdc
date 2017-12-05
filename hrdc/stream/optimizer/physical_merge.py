from .base import Optimizer

class PhysicalMerge(Optimizer): 
    precedence = 50

    def __init__(self, stream):
        from ..item import Item, GlobalItem,\
             LogicalMaximum, LogicalMinimum,\
             PhysicalMaximum, PhysicalMinimum

        self.stream = stream
        self.current = {
            GlobalItem.LogicalMinimum: LogicalMinimum(0),
            GlobalItem.LogicalMaximum: LogicalMaximum(0),
            GlobalItem.PhysicalMinimum: PhysicalMinimum(0),
            GlobalItem.PhysicalMaximum: PhysicalMaximum(0),
            }
        self.changed = dict(list(self.current.items()))
        self.pending = []

    def append(self, item):
        from ..item import Item, GlobalItem, PhysicalMinimum, PhysicalMaximum

        if item.kind == Item.Main:
            if int(self.current[GlobalItem.PhysicalMinimum].value) == 0 \
                and int(self.current[GlobalItem.PhysicalMaximum].value) == 0 \
                and int(self.changed[GlobalItem.PhysicalMinimum].value) \
                == int(self.changed[GlobalItem.LogicalMinimum].value) \
                and int(self.changed[GlobalItem.PhysicalMaximum].value) \
                == int(self.changed[GlobalItem.LogicalMaximum].value):
                self.pending = [x for x in self.pending
                                if x.kind != Item.Global
                                or x.tag not in (GlobalItem.PhysicalMinimum,
                                                  GlobalItem.PhysicalMaximum)]
            for i in self.pending:
                self.stream.append(i)
            self.pending = []
            self.changed = dict(list(self.current.items()))
            self.stream.append(item)
        else:
            self.pending.append(item)

            if item.kind == Item.Global \
                   and item.tag in (GlobalItem.LogicalMinimum,
                                    GlobalItem.LogicalMaximum,
                                    GlobalItem.PhysicalMinimum,
                                    GlobalItem.PhysicalMaximum):
                self.changed[item.tag] = item

    def __del__(self):
        for i in self.pending:
            self.stream.append(i)
