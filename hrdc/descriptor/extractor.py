from ..stream import Stream
from ..stream import item
from .. import usage
from .descriptor import *
from .descriptor import Hierarchical

class Extractor(Stream):
    def __init__(self):
        self.globals = {}
        for kind, tag in item.Item.registry.keys():
            if kind == item.Item.Global:
                self.globals[int(tag)] = 0
        self.localsClear()
        self.stack = []
        self.currentLevel = TopLevel()
        self.inNamedArrayCollection = False

    def localsClear(self):
        self.usages = []
        self.strings = []
        self.designators = []
        self.locals = {}

        for tag in (item.LocalItem.UsageMinimum, item.LocalItem.UsageMaximum,
                    item.LocalItem.DesignatorMinimum, item.LocalItem.DesignatorMaximum,
                    item.LocalItem.StringMinimum, item.LocalItem.StringMaximum,
                    item.LocalItem.Delimiter):
            self.locals[int(tag)] = None

    def globalValue(self, tag):
        return self.globals.get(int(tag), 0)

    def localValue(self, tag):
        return self.locals.get(int(tag), 0)

    def usage(self, index = 0):
        if not self.usages:
            return None
        u = self.usages[min((len(self.usages) - 1, int(index)))]
        if u >> 16:
            return u
        return usage.Usage.lookup((self.globals[int(item.GlobalItem.UsagePage)] << 16) | u)

    def string(self, index = 0):
        if not self.strings:
            return 0
        return self.strings[min((len(self.strings) - 1, int(index)))]

    def designator(self, index = 0):
        if not self.designators:
            return 0
        return self.designators[min((len(self.designators) - 1, int(index)))]

    def append(self, i):
        """Stream entry point"""
        try:
            self._append(i)
        except Exception as e:
            print("Exception while appending item", i)
            print("globals", self.globals)
            print("locals", self.locals)
            print("usages", self.usages)
            print("strings", self.strings)
            print("designators", self.designators)
            raise

    def _append(self, i):
        if i.kind == item.Item.Global:
            self.globals[int(i.tag)] = i.value

        elif i.kind == item.Item.Local:
            if i.tag == item.LocalItem.Usage:
                self.usages.append(i.value)

            elif i.tag == item.LocalItem.DesignatorIndex:
                self.designators.append(i.value)

            elif i.tag == item.LocalItem.StringIndex:
                self.strings.append(i.value)

            else:
                self.locals[int(i.tag)] = i.value

        elif i.kind == item.Item.Main:
            # Expand ranges
            for min, max, target in [
                (item.LocalItem.UsageMinimum, item.LocalItem.UsageMaximum, self.usages),
                (item.LocalItem.DesignatorMinimum, item.LocalItem.DesignatorMaximum, self.designators),
                (item.LocalItem.StringMinimum, item.LocalItem.StringMaximum, self.strings),
                ]:
                if self.locals[int(min)] is not None and self.locals[int(max)] is not None and not target:
                    for val in range(self.locals[int(min)], self.locals[int(max)] + 1):
                        target.append(val)

            if i.tag == item.MainItem.Collection:
                self.enter(i.value, self.usage())

            elif i.tag == item.MainItem.EndCollection:
                if self.inNamedArrayCollection:
                    self.inNamedArrayCollection = False
                else:
                    self.leave(self.currentLevel)

                if len(self.stack) == 0:
                    self.reportIdMerge(self.currentLevel)
                    self.ended(self.currentLevel)
                    
            elif i.tag in (item.MainItem.Input,
                           item.MainItem.Output,
                           item.MainItem.Feature):
                self.handleDataItem(i)

            self.localsClear()

    def enter(self, kind, usage):
        self.stack.append(self.currentLevel)
        self.currentLevel = Collection(kind, usage)

    def leave(self, level = None):
        self.currentLevel = self.stack.pop()
        if level:
            self.reportIdMerge(level)
            self.currentLevel.append(level)

    def reportIdMerge(self, level):
        level.__report_ids = set()
        for child in level.members:
            level.__report_ids |= child.__report_ids

    def addValue(self, v):
        v.__report_ids = set([int(self.globalValue(item.GlobalItem.ReportID))])
        self.currentLevel.append(v)

    def ended(self, root):
        self.root = root
        self.root = self.reportInsert(self.root)

        if len(self.root) == 1 and isinstance(self.root.members[0], TopLevel):
            self.root = self.root.members[0]

    def reportInsert(self, level):
        assert isinstance(level, Hierarchical)

        if isinstance(level, TopLevel):
            r = TopLevel()
        elif isinstance(level, Collection):
            r = Collection(level.kind, level.usage)
        else:
            raise ValueError(level)

        currentReport = None

        for value in level.members:
            if len(value.__report_ids) == 1 or isinstance(value, Value):
                if not currentReport or currentReport.id not in value.__report_ids:
                    currentReport = Report(list(value.__report_ids)[0])
                    r.append(currentReport)

                currentReport.append(value)

            else:
                assert isinstance(value, Hierarchical)
                currentReport = None
                r.append(self.reportInsert(value))

        return r

    def handleDataItem(self, i):
        if i.value & item.DataItem.Constant:
            self.addValue(Padding(i.tag, self.globalValue(item.GlobalItem.ReportSize)
                                          * self.globalValue(item.GlobalItem.ReportCount)))

        elif (self.globalValue(item.GlobalItem.ReportCount) == 1
              and len(self.usages) == (self.globalValue(item.GlobalItem.LogicalMaximum)
                                       - self.globalValue(item.GlobalItem.LogicalMinimum) + 1)
              and ((i.value == item.DataItem.Variable
                    and self.currentLevel.kind == Collection.NamedArray)
                   or (i.value == item.DataItem.Array
                       and self.currentLevel.kind == Collection.Logical
                       and usage.NAry.test(self.currentLevel.usage))
                   or (self.currentLevel.kind == Collection.Logical
                       and usage.NAry.test(self.currentLevel.usage)))):

            self.inNamedArrayCollection = True
            arrayCollection = self.currentLevel
            self.leave()
            assert len(arrayCollection) == 0

            uArray = list(map(self.usage, list(range(len(self.usages)))))
            try:
                uArray = usage.UsageRange.from_array(uArray)
            except ValueError:
                pass

            self.addValue(
                Value(i.tag, arrayCollection.usage,
                      self.globalValue(item.GlobalItem.ReportSize),
                      logicalMin = self.globalValue(item.GlobalItem.LogicalMinimum),
                      namedArray = uArray,
                      designator = self.designator(),
                      string = self.string(),
                      )
                )

        # Named array without enclosing collection (like in Keyboard RD)
        elif i.value == (item.DataItem.Data | item.DataItem.Array) and \
                 len(self.usages) == (self.globalValue(item.GlobalItem.LogicalMaximum)
                                      - self.globalValue(item.GlobalItem.LogicalMinimum) + 1):

            uArray = list(map(self.usage, list(range(len(self.usages)))))
            try:
                uArray = usage.UsageRange.from_array(uArray)
            except ValueError as e:
                print(e)
                pass
            for no in range(self.globalValue(item.GlobalItem.ReportCount)):
                self.addValue(
                    Value(i.tag, usage = None,
                          size = self.globalValue(item.GlobalItem.ReportSize),
                          logicalMin = self.globalValue(item.GlobalItem.LogicalMinimum),
                          namedArray = uArray,
                          designator = self.designator(),
                          string = self.string(),
                          )
                    )

        elif i.value & item.DataItem.BufferedBytes:

            ue = self.globalValue(item.GlobalItem.UnitExponent)
            self.addValue(
                Value(i.tag, self.usage(),
                      self.globalValue(item.GlobalItem.ReportSize),
                      flags = i.value,
                      logicalMin = self.globalValue(item.GlobalItem.LogicalMinimum),
                      logicalMax = self.globalValue(item.GlobalItem.LogicalMaximum),
                      physicalMin = self.globalValue(item.GlobalItem.PhysicalMinimum),
                      physicalMax = self.globalValue(item.GlobalItem.PhysicalMaximum),
                      designator = self.designator(),
                      string = self.string(),
                      unit = self.globalValue(item.GlobalItem.Unit),
                      unitExponent = ue,
                      count = self.globalValue(item.GlobalItem.ReportCount),
                      )
                )
    
        else:

            for n in range(self.globalValue(item.GlobalItem.ReportCount)):
                self.addValue(
                    Value(i.tag, self.usage(n),
                          self.globalValue(item.GlobalItem.ReportSize),
                          flags = i.value,
                          logicalMin = self.globalValue(item.GlobalItem.LogicalMinimum),
                          logicalMax = self.globalValue(item.GlobalItem.LogicalMaximum),
                          physicalMin = self.globalValue(item.GlobalItem.PhysicalMinimum),
                          physicalMax = self.globalValue(item.GlobalItem.PhysicalMaximum),
                          designator = self.designator(n),
                          string = self.string(n),
                          unit = self.globalValue(item.GlobalItem.Unit),
                          unitExponent = self.globalValue(item.GlobalItem.UnitExponent),
                          )
                    )

def main():
    import sys
    import argparse
    from ..stream import parser

    cmdline = argparse.ArgumentParser(description='Decompile a HID report descriptor')

    cmdline.add_argument("-i", "--input-format", metavar = "NAME", type = str,
                        default = "binary", help = "Input parser name")

    cmdline.add_argument("input", type = argparse.FileType('r'),
                         default = "-",
                         nargs = "?", help = "Input file name")

    cmdline.add_argument("output", type = argparse.FileType('w'),
                         default = "-",
                         nargs = "?", help = "Output file name")

    args = cmdline.parse_args()

    _parser = parser.Parser.get(args.input_format)

    extractor = Extractor()

    p = _parser(args.input, extractor)
    p.read()

    from .dumper import Dumper
    extractor.root.accept(Dumper(args.output))


if __name__ == "__main__":
    main()
