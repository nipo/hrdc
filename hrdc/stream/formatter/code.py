from .base import Formatter

class Code(Formatter):
    def __init__(self, output):
        self.indent = 0
        self.output = output
        
    def append(self, i):
        from ...stream import item

        blob = ", ".join(["0x%02x" % x for x in i.bytes()]) + ","
        if isinstance(i, item.EndCollection):
            self.indent -= 1
        self.output.write("     " + blob.ljust(6 * 5) + " // " + (" " * self.indent * 4) + str(i) + "\n")
        if isinstance(i, item.Collection):
            self.indent += 1
                          
                          
