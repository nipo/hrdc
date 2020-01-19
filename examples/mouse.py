from hrdc.usage import *
from hrdc.descriptor import *

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


if __name__ == "__main__":
    compile_main(mouse)
    
