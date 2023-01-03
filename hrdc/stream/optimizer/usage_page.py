from .base import Optimizer

class UsagePage(Optimizer):
    precedence = 10

    def __init__(self, stream):
        self.stream = stream
        self.page = None

    def append(self, item):
        from ..item import Item, GlobalItem, LocalItem, UsagePage, Usage
        from ...util import NamedConstant
        from ...usage import Usage

        if item.kind == Item.Local and item.tag in (LocalItem.Usage, LocalItem.UsageMinimum, LocalItem.UsageMaximum):

            sp, su = Usage.lookup(item.value).split()

            if self.page is None or self.page != int(sp):
                self.page = int(sp)
                self.stream.append(UsagePage(sp))

            item = Item.itemclass(item.kind, item.tag)(su)

        self.stream.append(item)

        if item.kind == Item.Global and item.tag == GlobalItem.UsagePage:
            self.page = int(item.value)

    def close(self):
        self.stream.close()
