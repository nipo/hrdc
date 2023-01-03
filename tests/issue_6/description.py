from hrdc.usage import *
from hrdc.descriptor import *
from hrdc.stream import formatter
from hrdc.stream import optimizer

mouse = Collection(Collection.Application, desktop.Mouse,
                   Value(Value.Input, desktop.X, 8,
                         flags = Value.Variable | Value.Relative,
                         logicalMin = -127, logicalMax = 127),
                   Value(Value.Input, desktop.Y, 8,
                         flags = Value.Variable | Value.Relative,
                         logicalMin = -127, logicalMax = 127),
                   Value(Value.Input, button.Button(1), 1,
                         logicalMin = 0, logicalMax = 1),
                   Value(Value.Input, button.Button(2), 1,
                         logicalMin = 0, logicalMax = 1),
                   Value(Value.Input, button.Button(3), 1,
                         logicalMin = 0, logicalMax = 1),
                   )

class HexList(formatter.Formatter):
    def __init__(self, output):
        self.output = output

    def append(self, i):
        blob = " ".join(["%02x" % x for x in i.bytes()])
        self.output.append(blob + "\n")

_list = []
_output = HexList(_list)
_output = optimizer.Optimizer.new(_output)
_visitor = streamer.Streamer(_output)
mouse.accept(_visitor)
if hasattr(_output, "close"):
    _output.close()
else:
    del _visitor
    del _output
print(''.join(_list))
