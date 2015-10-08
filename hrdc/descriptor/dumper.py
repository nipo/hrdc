import descriptor
from ..stream import item
from ..usage import Usage, UsageRange
from ..util import NamedConstant
import sys
import re

__all__ = ["Dumper"]

class Dumper(descriptor.Visitor):
    def __init__(self, output = sys.stdout):
        self.report_id = 0
        self.__indent = 0
        self.__output = output

    def write(self, *data):
        self.__output.write(" ".join(map(str, data)))

    def indent(self, offset = 0):
        return " " * ((self.__indent + offset) * 4)

    def enter(self, e):
        if self.__indent == 0:
            self.write("""from hrdc.usage import *
from hrdc.descriptor import *

descriptor = """)

        if isinstance(e, descriptor.TopLevel):
            self.write(self.indent() + "TopLevel(\n")

            self.__indent += 1
        elif isinstance(e, descriptor.Report):
            self.write(self.indent() + "Report(%d,\n" % (e.id))

            self.__indent += 1
        elif isinstance(e, descriptor.Collection):
            self.write(self.indent() + "Collection(Collection.%s, %s,\n" % (e.kind, Usage.lookup(e.usage) if e.usage is not None else None))
            
            self.__indent += 1

    def leave(self, e):
        if isinstance(e, (descriptor.Collection, descriptor.TopLevel, descriptor.Report)):
            self.__indent -= 1
            self.write(self.indent() + ")" + ("," if self.__indent else "") + "\n")

        if self.__indent == 0:
            self.write("""
if __name__ == "__main__":
    compile_main(descriptor)
""")

    def element(self, e):
        if isinstance(e, descriptor.Align):
            self.write(self.indent() + "Align(Value.%s, %d)," % (e.way, e.boundary)+"\n")

        elif isinstance(e, descriptor.Padding):
            self.write(self.indent() + "Padding(Value.%s, %d)," % (e.way, e.size)+"\n")

        elif isinstance(e, descriptor.Value):
            us = Usage.lookup(e.usage) if e.usage else None
            self.write(self.indent() + "Value(Value.%s, %s, %d" % (e.way, us, e.size))
            if int(e.flags) != int(item.DataItem.Data | item.DataItem.Variable | item.DataItem.Absolute) \
                   and not (e.namedArray and e.usage and e.flags == item.DataItem.Variable) \
                   and not (e.namedArray and not e.usage and e.flags == item.DataItem.Data | item.DataItem.Array):
                flags = str(e.flags)
                flags = re.sub(r"([A-Za-z]+)", r"Value.\1", flags)
                self.write(", flags = %s" % flags)
#            self.write(", reportId = %s" % list(e._Extractor__report_ids)[0])
            if e.logicalMin != 1:
                self.write(", logicalMin = %s" % e.logicalMin)
            if isinstance(e.namedArray, UsageRange):
                self.write(", namedArray = %s" % e.namedArray)
            elif e.namedArray != None:
                self.write(", namedArray = [\n")
                for u in e.namedArray:
                    self.write(self.indent(1) + str(u) + ",\n")
                self.write(self.indent(1) + "]")
            else:
                if e.logicalMax != None:
                    self.write(", logicalMax = %s" % e.logicalMax)
                if e.physicalMin != e.logicalMin or e.physicalMax != e.logicalMax:
                    if e.physicalMin != None:
                        self.write(", physicalMin = %s" % e.physicalMin)
                    if e.physicalMax != None:
                        self.write(", physicalMax = %s" % e.physicalMax)
            if e.unit != 0:
                unit = re.sub(r"([A-Za-z]+)", r"Unit.\1", str(e.unit))
                self.write(", unit = %s" % unit)
            if e.unitExponent != 0:
                self.write(", unitExponent = %s" % e.unitExponent)
            if e.designator != 0:
                self.write(", designator = %s" % e.designator)
            if e.string != 0:
                self.write(", string = %s" % e.string)
            if e.count != 1:
                self.write(", count = %d" % e.count)
            auto_alignment = min((8, e.size))
            if e.alignment != None and e.alignment != auto_alignment:
                self.write(", alignment = %s" % e.alignment)
            self.write("),\n")
