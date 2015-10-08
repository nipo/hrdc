from ..stream import Stream
from .. import item
from ... import usage

class Parser(Stream):
    class __metaclass__(type):
        def __init__(cls, name, bases, dct):
            type.__init__(cls, name, bases, dct)
            try:
                Parser.registry[cls.__name__.lower()] = cls
            except:
                pass

    registry = {}

    @classmethod
    def get(cls, name):
        return cls.registry[name]

    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.usagePage = 0

    def blobParse(self, blob):
        while blob:
            header = blob[0]
            size = ord(header) & 0x3
            data_size = (1 << (size - 1)) + 1 if size else 1
            item = blob[:data_size]
            blob = blob[data_size:]
            self.itemParse(item)

    def itemParse(self, data):
        self.append(item.Item.parse(data))

    def append(self, i):
        if i.kind == item.Item.Global and i.tag == item.GlobalItem.UsagePage:
            self.usagePage = int(i.value)
            i = item.UsagePage(usage.Usage.page(i.value))

        if i.kind == item.Item.Local \
               and i.tag in (item.LocalItem.Usage, item.LocalItem.UsageMinimum, item.LocalItem.UsageMaximum) \
               and (int(i.value) >> 16) == 0:
            i = item.Item.itemclass(i.kind, i.tag)(usage.Usage.inpage(self.usagePage, i.value))

        self.output.append(i)

