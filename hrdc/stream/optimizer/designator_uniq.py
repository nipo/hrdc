from .base import Optimizer

class DesignatorUniq(Optimizer):
    precedence = 70

    def __init__(self, stream):
        from ..item import Item, LocalItem, DesignatorIndex, \
             DesignatorMinimum, DesignatorMaximum

        self.stream = stream
        self.pending = []
        self.designatorToFilter = None

    def append(self, item):
        from ..item import Item, LocalItem, DesignatorIndex, \
             DesignatorMinimum, DesignatorMaximum

        self.pending.append(item)

        if item.kind == Item.Local:
            if item.tag == LocalItem.DesignatorIndex:
                if self.designatorToFilter is None and int(item.value) == 0:
                    self.designatorToFilter = item
                else:
                    self.designatorToFilter = False
        else:
            if self.designatorToFilter:
                self.pending = [x for x in self.pending if x is not self.designatorToFilter]
            for i in self.pending:
                self.stream.append(i)
            self.pending = []
            self.designatorToFilter = None
            
