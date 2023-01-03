from .base import Optimizer

class MainMerge(Optimizer):
    precedence = 60

    from ..item import Item, GlobalItem, LocalItem, MainItem
    to_watch = (
        GlobalItem.LogicalMinimum,
        GlobalItem.LogicalMaximum,
        GlobalItem.PhysicalMinimum,
        GlobalItem.PhysicalMaximum,
        GlobalItem.Unit,
        GlobalItem.UnitExponent,
        GlobalItem.ReportSize,
        GlobalItem.ReportID,
        )

    def __init__(self, stream):
        self.stream = stream
        self.beforeMain = []
        self.mainItems = []
        self.afterMain = []
        self.beforeCount = 0
        self.afterCount = 0
        
        self.props = {}
        
        for key in self.to_watch:
            self.props[key] = 0

    def append(self, item):
        from ..item import Item, MainItem, GlobalItem

        if item.kind == Item.Local:
            self.afterMain.append(item)

        elif item.kind == Item.Global:
            self.afterMain.append(item)

            if item.tag in self.to_watch:
                if self.props.get(item.tag, int(item.value)) != int(item.value):
                    self.props[item.tag] = int(item.value)
                    self.flush()

            if item.tag == GlobalItem.ReportCount:
                self.afterCount = item.value

        else:
            if item.tag not in (MainItem.Input, MainItem.Output, MainItem.Feature):
                self.afterMain.append(item)
                self.flush()
                return

            if self.mainItems and item != self.mainItems[0]:
                self.flush()

            flush_after = self.afterCount != 1

            self.beforeMain += self.afterMain
            self.beforeCount += self.afterCount
            self.afterMain = []
            self.mainItems.append(item)

            if flush_after:
                self.flush()

    def flush(self, until = 0):
        from ..item import ReportCount, Item, MainItem, GlobalItem

        for i in self.beforeMain:
            if i.kind != Item.Global or i.tag != GlobalItem.ReportCount:
                self.stream.append(i)

        if self.mainItems:
            self.stream.append(ReportCount(self.beforeCount))
            self.stream.append(self.mainItems[0])

        self.beforeMain = self.afterMain
        self.mainItems = []
        self.afterMain = []
        self.beforeCount = 0

    def close(self):
        for i in self.beforeMain:
            self.stream.append(i)
        for i in self.mainItems:
            self.stream.append(i)
        for i in self.afterMain:
            self.stream.append(i)
        self.stream.close()
