import descriptor
from ..stream import item

__all__ = ["Streamer"]

class Streamer(descriptor.Visitor):
    def __init__(self, stream):
        self.stream = stream
        self.report_size = {
            int(item.MainItem.Input) : [0] * 256,
            int(item.MainItem.Output) : [0] * 256,
            int(item.MainItem.Feature) : [0] * 256,
            }
        self.report_id = 0

    def enter(self, e):
        a = self.stream.append

        if isinstance(e, descriptor.Report):
            self.report_id = e.id
            if e.id:
                a(item.ReportID(e.id))

        elif isinstance(e, descriptor.Collection):
            a(item.Usage(e.usage))
            a(item.Collection(e.kind))

    def leave(self, e):
        a = self.stream.append

        if isinstance(e, descriptor.Collection):
            a(item.EndCollection())

    def element(self, e):
        a = self.stream.append
        align = 0
        pad = 0

        if isinstance(e, descriptor.Align):
            align = e.boundary

        elif isinstance(e, descriptor.Padding):
            pad = e.size

        elif isinstance(e, descriptor.Value):
            align = e.alignment

        if align > 1:
            current_size = self.report_size[int(e.way)][self.report_id]
            partial = current_size % align
            pad = (align - partial) if partial else 0

        if pad:
            a(item.ReportCount(1))
            a(item.ReportSize(pad))
            self.report_size[int(e.way)][self.report_id] += pad
            a(item.Item.itemclass(item.Item.Main, e.way)(item.DataItem.Constant | item.DataItem.Variable))

        if isinstance(e, descriptor.Value) and not isinstance(e, descriptor.Align):
            constant = bool(e.flags & item.DataItem.Constant)
            if not constant:
                if e.usage:
                    a(item.Usage(e.usage))
    
                if e.namedArray:
                    a(item.PhysicalMinimum(0))
                    a(item.PhysicalMaximum(0))
                    if e.usage:
                        a(item.Collection(item.Collection.Logical))
                    for usage in e.namedArray:
                        a(item.Usage(usage))

                elif e.physicalMin == e.logicalMin and e.physicalMax == e.logicalMax:
                    a(item.PhysicalMinimum(0))
                    a(item.PhysicalMaximum(0))
                else:
                    a(item.PhysicalMinimum(e.physicalMin))
                    a(item.PhysicalMaximum(e.physicalMax))

                a(item.LogicalMinimum(e.logicalMin))
                a(item.LogicalMaximum(e.logicalMax))

                a(item.Unit(e.unit))
                a(item.UnitExponent(e.unitExponent))
                if int(e.designator):
                    a(item.DesignatorIndex(e.designator))
                if int(e.string):
                    a(item.StringIndex(e.string))

            a(item.ReportCount(e.count))
            a(item.ReportSize(e.size))
            self.report_size[int(e.way)][self.report_id] += int(e.size)
            a(item.Item.itemclass(item.Item.Main, e.way)(e.flags))

            if e.namedArray and not constant and e.usage:
                a(item.EndCollection())
